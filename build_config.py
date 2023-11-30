#!/usr/bin/python

import jinja2
import yaml
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=">>> Juniper Jinja2 Template conversion tool")
    parser.add_argument(
        "--template",
        required=True,
        type=str,
        help="Specify the Junos configuration template file",
    )
    parser.add_argument(
        "--variables",
        required=True,
        type=str,
        help="Specify the YAML variable file",
    )
    parser.add_argument(
        "--out",
        required=False,
        type=str,
        help="Specify filename to send configuration output instead of the default to screen"
    )
    args = parser.parse_args()

    with open(args.variables) as fh:
        yaml_vars = yaml.load(fh.read(), Loader=yaml.Loader)
        
    with open(args.template) as fh:
        jinja2_template = jinja2.Template(fh.read())

    configuration = jinja2_template.render(yaml_vars['variables'])

    if args.out :
        with open(args.out, "x") as out:
            out.write(configuration)
        with open(args.out, 'r') as out:
            for lines, line in enumerate(out):
                pass
        print('\n',lines + 1,'Lines written to file')
    else :
        print(configuration)
    
    print("\nConfiguration has been succesfully created... \nUse `load merge terminal` on CLI to apply configuration")
