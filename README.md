# lambda-customresource
A helper object to create AWS Cloudformation Lambda-backed CustomResources in python

Please see example in handler.py. Update example.template accordingly.

``` shell
./build_lambda_zip.sh
aws s3 cp ./handler.zip s3://bucket/prefix/
aws s3 cp ./example.template s3://bucket/prefix/
aws cloudformation create-stack --stack-name somestack \
    --template-url https://s3.amazonaws.com/bucket/prefix/example.template \
    --capabilities CAPABILITY_IAM
```
