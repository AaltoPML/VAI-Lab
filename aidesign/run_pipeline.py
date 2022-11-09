"""
CLI for running a pipeline from a config file 
or start a GUI if no config file given. 
"""

import argparse

import aidesign as ai



def parse_args():
    """
    Parse command line arguments
    """

    parser = argparse.ArgumentParser(
                        prog = 'aidesign',
                        description = 'AI-assisted virtual laboratories',
                        )

    parser.add_argument(
                        '-f', 
                        '--file',
                        type=str,
                        nargs='+',
                        default=None,
                        help='pipeline config file',                        
                        )

    args = parser.parse_args()

    return args



def main():

    # Parse command line arguments
    args = parse_args()

    # Core instance
    core = ai.Core()

    # Load config file if given
    if args.file:
        core.load_config_file(args.file)

    # Run pipeline   
    core.run()



if __name__=='__main__':

    main()