"""
CLI for running a pipeline from a config file 
or start a GUI if no config file given. 
"""

import argparse
from pathlib import Path 

import vai_lab as ai



def parse_args():
    """
    Parse command line arguments
    """

    parser = argparse.ArgumentParser(
                        prog = 'vai_lab',
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

def _config_files_iter(core,files):
    """Iterate over config files and load them into core
    TODO: WIP - need a reset function to avoid instantiating core every time
    """
    if files:
        for f in files:
            core = ai.Core()
            core.load_config_file(Path(f).resolve())
            core.run()


def main():

    # Parse command line arguments
    args = parse_args()

    # Core instance
    core = ai.Core()

    # Load config file if given
    if args.file:
        args.file = [Path(f).resolve() for f in args.file]
        core.load_config_file(args.file)

    # Run pipeline   
    core.run()

if __name__=='__main__':
    
    main()