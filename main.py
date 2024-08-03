from src.cnnClassifier import logger
from src.cnnClassifier.pipeline.data_ingestion_stage_01 import DataIngestionTrainingPipeline



STAGE_NAME = "Data Ingestion stage"


try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(f"Exception occurred during {STAGE_NAME}: {str(e)}")
    raise e