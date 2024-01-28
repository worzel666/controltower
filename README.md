## About The Project


At the time of writing this, Control Tower's public API is very limited.
This 'library' helps to make automating Control Tower a bit more accessible,
and a bit more like a native Boto3 client.

Example usage:
```
import controltower

controltower.describe_managed_organizational_unit(
    OrganizationalUnitId="ou-1234-abcd",
    OrganizationalUnitName="My-OU",
)
```

With exceptions courtesy of botocore!
For example, the above:
```
An error occurred (ResourceNotFoundException) when calling the DescribeManagedOrganizationalUnit operation: AWS Control Tower could not find a registered OU with ID 'ou-1234-abcd' for account '123412341234' .
```
