import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },
    "trait": {
        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },
        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },
        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },
    # Mutation probability
    "mutation": 0.01
}

def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = list(people.keys())  # Convert to list for consistent indexing
    for have_trait in powerset(names):
        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")

def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data

def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def compute_gene_probability(people, person, num_genes, one_gene, two_genes):
    """
    Compute the probability of the given number of genes for a person.
    """
    if person not in people:
        return 0

    if people[person]['mother'] is None:
        return PROBS['gene'][num_genes]

    father = people[person]['father']
    mother = people[person]['mother']

    # Probability of passing on genes from parents
    passing_on = {
        0: (1 - PROBS['mutation']) ** 2,
        1: 2 * (1 - PROBS['mutation']) * PROBS['mutation'],
        2: PROBS['mutation'] ** 2
    }

    # Probability of person inheriting genes from parents
    if father in one_gene:
        inherited_from_father = 0.5
    elif father in two_genes:
        inherited_from_father = 1 - PROBS['mutation']
    else:
        inherited_from_father = PROBS['mutation']

    if mother in one_gene:
        inherited_from_mother = 0.5
    elif mother in two_genes:
        inherited_from_mother = 1 - PROBS['mutation']
    else:
        inherited_from_mother = PROBS['mutation']

    if num_genes == 0:
        probability = (1 - inherited_from_father) * (1 - inherited_from_mother)
    elif num_genes == 1:
        probability = (1 - inherited_from_father) * inherited_from_mother + inherited_from_father * (1 - inherited_from_mother)
    else:
        probability = inherited_from_father * inherited_from_mother

    return probability



def compute_trait_probability(people, person, num_genes, have_trait):
    """
    Compute the probability of the person exhibiting the trait.
    """
    if person not in people:
        return 0

    trait_prob_given_genes = PROBS['trait'][num_genes]

    if have_trait:
        return trait_prob_given_genes[True]
    else:
        return trait_prob_given_genes[False]

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute the joint probability of the people having the specified gene and trait combinations.
    """
    # Initialize joint probability
    joint_prob = 1

    # Loop through each person
    for person in people:
        # Get the number of genes the person has
        num_genes = 0
        if person in one_gene:
            num_genes = 1
        elif person in two_genes:
            num_genes = 2

        # Get whether the person has the trait
        person_has_trait = person in have_trait

        # Compute the probability of the person having the specified gene and trait combinations
        gene_prob = compute_gene_probability(people, person, num_genes, one_gene, two_genes)
        trait_prob = compute_trait_probability(people, person, num_genes, person_has_trait)

        # Update the joint probability
        joint_prob *= gene_prob * trait_prob

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    """
    for person in probabilities:
        num_genes = 0
        if person in one_gene:
            num_genes = 1
        elif person in two_genes:
            num_genes = 2

        has_trait = person in have_trait

        probabilities[person]["gene"][num_genes] += p
        probabilities[person]["trait"][has_trait] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution is normalized.
    """
    for person in probabilities:
        for field in probabilities[person]:
            total = sum(probabilities[person][field].values())
            for value in probabilities[person][field]:
                probabilities[person][field][value] /= total

if __name__ == "__main__":
    main()
