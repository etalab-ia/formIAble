"""
Module allowing to generate samples for a given cerfa
"""
import argparse
from src.util.dataGeneration import Writer

def run(num_cerfa, nb_samples=10):
    """
    Generate samples for a given cerfa
    :param str num_cerfa: Cerfa number we want to generate (The empty template and the config json file must be
    present in data/CERFA/toFill)
    :param int nb_samples: Number of pdf to generate
    :return: None
    """
    sub_writers = Writer.__subclasses__()
    matching_writers = [w for w in sub_writers if num_cerfa in w.__name__]
    if len(matching_writers)>1:
        raise ValueError(f"Ambiguous cerfa number: {num_cerfa}, multiple writers are matching:\n"
                         f"{[w.__name__ for w in matching_writers]}")
    elif len(matching_writers)==1:
        custom_writer = matching_writers[0]

        for idx in range(nb_samples):
            writer = custom_writer( num_cerfa = num_cerfa)
            writer.fill_form()
            writer.save()
    else:
        raise ValueError(f"No custom writer found for cerfa : {num_cerfa}. Available writers are:\n"
                         f"{[w.__name__ for w in sub_writers]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('num_cerfa', type=str, nargs=1,
                        help='The cerfa number')
    parser.add_argument('--nb_samples', default=10, type=int,
                        help='The number of samples to generate for each cerfa')

    args = parser.parse_args()

    run(num_cerfa = args.num_cerfa[0], nb_samples = vars(args)['nb_samples'])

