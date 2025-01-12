# JunOS Configuration Templates

Juniper configuration templates for some very common configurations formatted in jinja2.

Theses files are designed to be used in several ways:
1. By an Ansible system, using configuration load, 
2. Using the build_config.py script,
3. Or with manual substitution of the variables.

## Use

Create your own YAML Variable files using the examples included at the top of each jinja Template file.

Run the build_config.py in a Python environment 

Example: 

`python .\build_config.py --template .\remote_vpn.j2 --variables .\group_vars\RTR1.yml [--out .\configs\remote-vpn-rtr1.conf]`

The Script uses functions from the jinja2 and yaml libraries to load these templates and your variables and render them together to output a finished configuration.

If no `--out ` is defined, the configuration is output to screen.

This finished configuration can be used directly on the JunOS CLI using `load merge terminal`, using `push_config.py` (See below), or instruct ansible to load the configuration for you.

NOTE: The `base_srx.j2` template is the exception to this as the Complex nesting of Security Policy configuration forced me to resort to `set` commands.

### Push Config
`push_config.py` Will connect to the device using SSH from your machine and load the configration for you. It will prompt you for Device Hostname, Username and Password. It will also ask for the path to the configuration file you wish to upload.

## Explainers

### Jinja2 templates
Examining some of the aspects of the Jinja2 templates:<ul>
    <li>Flow control and loop structures are enclosed in `{% %}`.</li>
    <li>Variables are defined in the jinja2 templates by the variable name enclosed in `{{  }}`.</li>
    <li>For loops are closed with `{% endfor %}`</li>
    <li>If Statements are closed with `{% endif %}`</li></ul>
    
### YAML Variable Files
Create your own YAML Variable files using the examples included at the top of each jinja Template file.

Example:
```
## ** variables.yml Example **
## VPN External Interface
#ext_int: ge-0/0/0
## VPN External Interface Zone
#ext_zone: untrust
## VPN DNS Hostname
#dns_hn: vpn.domain.com
## VPN PreShared-Key (IKE)
#vpn_psk: xxxyyyzzz
#local_subnets:
## List of Local Protected Subnets
#- {name: corp, subnet: 192.168.0.0, mask: 24}
#- {name: voice, subnet: 192.168.1.0, mask: 24}
```

Remove all of the first leading `#`'s from each line and update the values (those after the "key:") from each key value pair.

Result:
```yaml
# ** variables.yml Example **
# VPN External Interface
ext_int: ge-0/0/1
# VPN External Interface Zone
ext_zone: internet
# VPN DNS Hostname
dns_hn: vpn.widgets.com
# VPN PreShared-Key (IKE)
vpn_psk: aaabbbccc
local_subnets:
# List of Local Protected Subnets
- {name: corp, subnet: 192.168.10.0, mask: 24}
- {name: voice, subnet: 192.168.11.0, mask: 24}
```


### Configuration Groups
All configuration templates (with the exception of base configs) are appied as Configuration Groups...
e.g. 
```
groups {
    replace: group-name {
        ...
    }
}
apply-groups group-name;
```
Configuration Groups ease the deployment and cleanup of configuration templates by grouping them per "function". 
A group can be de/activated and added/removed without affecting the root configuration on the device.
Group Configurations are inherited by the root configuration using apply-groups {}, this is very flexible.
For more information on Configuration Groups see... https://www.juniper.net/documentation/us/en/software/junos/cli/topics/topic-map/configuration-groups-usage.html
