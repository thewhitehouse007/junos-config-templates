from collections import defaultdict

def remove_junos_defaults(data):
    """Clean the 'Applications' and 'Objects' sheets by removing specific entries."""
    # Remove rows from 'Applications' sheet where 'Name' is 'any*'
    if "Applications" in data:
        cleaned_list = [
            row for row in data["Applications"]
            if not (row.get("Name") == "any")  # Remove rows where 'Name' is 'any'
            and not (isinstance(row.get("Name"), str) and row["Name"].startswith("junos-"))  # Keep existing logic
        ]
        data["Applications"] = cleaned_list

    # Remove rows from 'Objects' sheet where 'Name' is 'any'
    if "Objects" in data:
        cleaned_list = [
            row for row in data["Objects"]
            if row.get("Name") != "any"  # Remove rows where 'Name' is 'any'
        ]
        data["Objects"] = cleaned_list

    # Remove the default 'global' zone from the sheet
    if "Zones" in data:
        cleaned_list = [
            row for row in data["Zones"]
            if row.get("Name") != "global"  # Remove rows where 'Name' is 'global'
        ]
        data["Zones"] = cleaned_list

# Function to merge policies with matching 'From Zone', 'To Zone', and 'Name'
def merge_policies(policies):
    merged_policies = {}
    
    for policy in policies:
        # Unique key based on 'From Zone', 'To Zone', and 'Name'
        key = (policy['From Zone'], policy['To Zone'], policy['Name'])
        
        if key not in merged_policies:
            # Initialize with a copy of the policy
            merged_policies[key] = {k: v for k, v in policy.items() if k not in ['Application', 'Source Address', 'Destination Address', 'Dynamic Application']}
            merged_policies[key]['Application'] = set()
            merged_policies[key]['Source Address'] = set()
            merged_policies[key]['Destination Address'] = set()
            if 'Dynamic Application' in policy: merged_policies[key]['Dynamic Application'] = set()
        else:
            # Keep the smallest Sequence number
            if 'Sequence' in policy and 'Sequence' in merged_policies[key]:
                merged_policies[key]['Sequence'] = min(merged_policies[key]['Sequence'], policy['Sequence'])
        
        # Check for conflicts in 'Action' and 'Enabled'
        if policy['Action'] != merged_policies[key]['Action'] or policy['Enabled'] != merged_policies[key]['Enabled']: ## TODO: Causes KeyError ??
            print(f"Conflict found for policy '{policy['Name']}' between zones '{policy['From Zone']}' and '{policy['To Zone']}'")
            print(f"Different values for 'Action' or 'Enabled' not allowed.")
            continue  # Skip merging this policy if there's a conflict

        # Add unique values to sets for 'Application', 'Dynamic Application', 'Source Address', and 'Destination Address'
        merged_policies[key]['Application'].add(policy['Application'].strip())
        merged_policies[key]['Source Address'].add(policy['Source Address'].strip())
        merged_policies[key]['Destination Address'].add(policy['Destination Address'].strip())
        if 'Dynamic Application' in policy : merged_policies[key]['Dynamic Application'].add(policy['Dynamic Application'].strip())
    
    # Convert sets back to sorted lists for final output
    for policy in merged_policies.values():
        policy['Application'] = sorted(policy['Application'])
        if 'Dynamic Application' in policy : policy['Dynamic Application'] = sorted(policy['Dynamic Application'])
        policy['Source Address'] = sorted(policy['Source Address'])
        policy['Destination Address'] = sorted(policy['Destination Address'])
    
    # Return as a list of merged policies
    return list(merged_policies.values())

# Function to set the specified Key the the specified Value if it does not exist
def set_default_value(objects, key, default):
    for obj in objects:
        if key not in obj:
            obj[key] = default
    return objects

# Grouping Object-Set by a defined Key-Value and removing the key
def group_lists_by(objects, key):
    grouped_by = defaultdict(list)
    for obj in objects:
        value = obj.pop(key, 'undefined')
        grouped_by[value].append(obj)
    return dict(grouped_by)

# Function to sort Lists by a Specified Key-value
def sort_list_by(list, key):
    def sort_key(obj):
        zone = obj.get(key, 'zzundefined')  # Use 'zzundefined' for missing Key to sort these last
        # Try to convert to integer; fall back to string if it fails
        try:
            return (0, int(zone))  # Numbers come first, sorted numerically
        except ValueError:
            return (1, zone)  # Strings come after numbers, sorted alphabetically
    
    # Sort using the custom key
    return sorted(list, key=sort_key)


def main(data):
    # Removes the default configuration that is included in JunOS
    remove_junos_defaults(data)
    
    # Sorted the Lists in each Table for easy to read JunOS configuration 
    data["Objects"] = sort_list_by(data.get('Objects', []),'Zone')
    data["Objects"] = set_default_value(data.get('Objects', []),'Zone','global')

    # Note: Sorts are in reverse with the highest priority last
    data["Policies"] = merge_policies(data.get('Policies', []))
    data["Policies"] = sort_list_by(data.get('Policies', []),'Sequence')
    data["Policies"] = sort_list_by(data.get('Policies', []),'To Zone')
    data["Policies"] = sort_list_by(data.get('Policies', []),'From Zone')

    data["NAT"] = sort_list_by(data.get('NAT', []),'Sequence')
    data["NAT"] = sort_list_by(data.get('NAT', []),'Type')
    
    data["Interfaces"] = sort_list_by(data.get('Interfaces', []),'Logical Unit')
    data["Interfaces"] = sort_list_by(data.get('Interfaces', []),'Interface')

    # Sets the Zones vrf to 'default' if it is not defined
    data["Zones"] = set_default_value(data.get('Zones', []),'vrf', 'default')
    data["Zones"] = sort_list_by(data.get('Zones', []),'Zone')

    return data
