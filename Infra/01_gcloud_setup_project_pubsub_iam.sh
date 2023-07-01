source .env

# Create new Project
gcloud projects create $PROJECT_ID --name=$PROJECT_NAME

# Create Service Account and grant access
gcloud iam service-accounts create $SERVICE_ACCOUNT
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/pubsub.subscriber"

# Deploy Cloud Run service
gcloud beta run deploy $SERVICE_NAME \
    --image $IMAGE \
    --service-account $SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com \
    #--allow-unauthenticated \
    --region $REGION \
    #--concurrency 1 \
    #--memory 256Mi
gcloud run services describe $SERVICE_NAME \
    #--platform=managed \
    --region=$REGION \
    #--format='value(status.url)'

# Create the PubSub topic
gcloud pubsub topics create $TOPIC_NAME
gcloud pubsub subscriptions create $SUBSCRIPTION_NAME \
    --topic=$TOPIC_NAME \
    --push-endpoint=$SERVICE_URL
