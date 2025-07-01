# JunOS Excel Templates

The following Excel Workbook templates are for planning for deployment of Network Devices (Although mostly Juniper we will try to keep them agnostic as possible). 

Theses workbooks are designed to be used in several ways:
1. Build base configuration values for network hardware
2. Plan and Build Security Policies 
3. Bulk import for address book or Security Policies
4. To aid in converstion from other formats of cofiguration output from other vendor devices.

## Use

Copy the "sample_workbook.xlsx" file then build and document your design/configuration.

Save the Excel Workbook then use the `excel_to_yaml.py` to convert to a YAML variable file, ready for processing by `build_config.py`

Example: 

`python .\excel_to_yaml.py --excel .\sample_workbook.xlsx --yaml ..\group_vars\base_srx.yml`

>NOTE: if no arguments are supplied the default values will use what is shown above.

The Script uses functions from the pandas and yaml libraries to collate and clean up entries from the excel templates and render the output as a YAML file that can then be used by the `build_config.py` script and the relevent Jinja2 templates.

Dependant Packages include (use 'pip install'):
* pandas
* openpyxl
* pyyaml

<!-- 
### Conversion from JunOS XML to Excel
`fw_xml_to_excel.py`  Allows for the conversion of existing JunOS Device configuration (only in XML) back to the Excel spreadsheet. To allow for the redocumentation or review of existing devices.
Currectly a work in progress!
-->

## Explainers

### Excel templates
Explaining some of the procedures for completing excel templates:<ul>
    <li>Fill the sheets in order to allow for Drop-Down menu functionality to work,</li>
    (Not Doing this, or entring values manually, will cause validation errors)
    <li>junOS Default values are cleared during converstion, do not edit them,</li>
    <li>Policies are enabled by default, unless specifically marked as disabled,</li>
    <li>Logging and Counting is disabled by default,</li>
    <li>Empty lines/rows are ignored.</li></ul>
    
### Excel Files
Some example Excel files available are:<ul>
    <li>SRX, NAT & Security Policy - [SHA256](## "ECEE3EF5BB0586CA55E1EFE69E060D96E10C3EE598EAFB57A06F4AC524F7412C")</li>
    <!-- <li>SRX, Site-to-Site IPSEC VPN,</li> -->
    </ul>
    

### Bug Reporting & Custom Solutions
Technology always changes and evolves, scenarios create new requirements...

If you have trouble using the excel workbooks or convertion tools here please post a bug report or feature request and I'll do my best to respond and resolve the issue.

If you have specific needs or would like assistance with your network solution, please reach out to us at sales@brightnet.com.au
