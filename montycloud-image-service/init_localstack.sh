#!/bin/bash
awslocal s3 mb s3://montycloud-image

awslocal dynamodb create-table   --table-name montycloud_images_metadata   --attribute-definitions     AttributeName=image_id,AttributeType=S     AttributeName=user_id,AttributeType=S   --key-schema AttributeName=image_id,KeyType=HASH   --global-secondary-indexes     '[{
      "IndexName":"user_id-index",
      "KeySchema":[{"AttributeName":"user_id","KeyType":"HASH"}],
      "Projection":{"ProjectionType":"ALL"}
    }]'   --billing-mode PAY_PER_REQUEST
