from fastapi import FastAPI, UploadFile, File, Query, HTTPException
import uuid, datetime
from mangum import Mangum
from app.aws import s3, table
from app.models import *
from typing import List, Optional
from boto3.dynamodb.conditions import Key

app = FastAPI(title="Image Upload Service")

BUCKET = "montycloud-image"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/images/upload", response_model=UploadImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    user_id: str = Query(...),
    tags: str = Query("")
):
    image_id = str(uuid.uuid4())
    s3_key = f"{user_id}/{image_id}"

    s3.upload_fileobj(
        file.file,
        BUCKET,
        s3_key,
        ExtraArgs={"ContentType": file.content_type}
    )

    table.put_item(
        Item={
            "image_id": image_id,
            "user_id": user_id,
            #"tags": tags.split(",") if tags else [],
            #"s3_key": s3_key,
            #"content_type": file.content_type,
            #"created_at": datetime.datetime.utcnow().isoformat()
        }
    )
    return {"image_id": image_id}


@app.get("/images", response_model=List[ImageListResponse])
def list_images(
    user_id: str = Query(..., example="user_123"),
    tag: Optional[str] = Query(None, example="travel"),
    from_date: Optional[str] = Query(None, example="2024-01-01T00:00:00"),
    to_date: Optional[str] = Query(None, example="2024-01-31T23:59:59")):
         
        """
        List images with optional filters:
        - user_id (required)
        - tag
        - date range
        """
    
        # Query DynamoDB using GSI
        response = table.query(
            IndexName="user_id-index",
            KeyConditionExpression=Key("user_id").eq(user_id)
        )
    
        items = response.get("Items", [])
    
        # Filter by tag
        if tag:
            items = [i for i in items if tag in i.get("tags", [])]
    
        # Filter by date range
        if from_date:
            from_dt = datetime.fromisoformat(from_date)
            items = [
                i for i in items
                if datetime.fromisoformat(i["created_at"]) >= from_dt
            ]
    
        if to_date:
            to_dt = datetime.fromisoformat(to_date)
            items = [
                i for i in items
                if datetime.fromisoformat(i["created_at"]) <= to_dt
            ]
    
        return items

@app.get("/images/{image_id}", response_model=ViewImageResponse)
def view_image(image_id: str):
    resp = table.get_item(Key={"image_id": image_id})
    if "Item" not in resp:
        raise HTTPException(404, "Image not found")

    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": resp["Item"]["s3_key"]},
        ExpiresIn=3600
    )
    return {"url": url}

@app.delete("/images/{image_id}", response_model=DeleteImageResponse)
def delete_image(image_id: str):
    resp = table.get_item(Key={"image_id": image_id})
    if "Item" not in resp:
        raise HTTPException(404, "Image not found")

    s3.delete_object(
        Bucket=BUCKET,
        Key=resp["Item"]["s3_key"]
    )
    table.delete_item(Key={"image_id": image_id})
    return {"message": "Deleted"}


handler = Mangum(app)