from pipelines.inference_pipeline import fraud_detection_inference_pipeline

if __name__ == "__main__":
    print("Starting Fraud Detection Batch Inference Pipeline...")
    
    # Execute the inference pipeline
    fraud_detection_inference_pipeline()
    
    print("\n✅ Batch inference completed successfully!")
