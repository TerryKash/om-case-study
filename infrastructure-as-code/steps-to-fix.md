# Add steps/actions here:

# Steps to Remove the 2nd Resource Without Unintended Recreations

## Step 1: Update Terraform Code to use `for_each` with explicit keys
Replace the `count` meta-argument with a map/set of explicit identifiers, omitting the 2nd resource (e.g., `item-2`):

locals {
  resources = toset(["res-1", "res-3", "res-4", "res-5"])
}

resource "example_resource" "this" {
  for_each = local.resources
  name     = "example-${each.key}"
}   

## Step 2: Migrate State Entries using moved blocks

moved {
  from = example_resource.this[0]
  to   = example_resource.this["res-1"]
}
moved {
  from = example_resource.this[2]
  to   = example_resource.this["res-3"]
}

# destroy index 1 manually 
terraform destroy -target='example_resource.this[1]'

