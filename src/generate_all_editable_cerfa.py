"""
Module allowing to generate samples for all cerfa templates present in data/CERFA/toFill
"""
import argparse

from util.dataGeneration import Writer

def run_all(nb_samples=10):
    """
    Generate samples for all cerfa templates present in data/CERFA/toFill
    :param int nb_samples: Number of pdf to generate
    :return: None
    """

    for subWriterClass in Writer.__subclasses__():
        subWriterClassName = subWriterClass.__name__
        num_cerfa = subWriterClassName.replace("Writer", '')

        for idx in range(nb_samples):
            writer = subWriterClass(num_cerfa=num_cerfa)
            writer.fill_form()
            writer.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--nb_samples', default=10, type=int,
                        help='The number of samples to generate for each cerfa')

    args = parser.parse_args()
    run_all(nb_samples = vars(args)['nb_samples'])

