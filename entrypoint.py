from src.clients.image_service_client import ImageServiceClient
from src.clients.queue_client import QueueClient
from src.clients.upscale_client import UpscaleClient
from src.processors.image_processor import ImageProcessor

import argparse
import yaml
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser(description='Process the queue of images to be upscaled')
    parser.add_argument('-c', '--config',
                        default='config.yml',
                        help='path to the config file to be loaded (default: config.yml')
    args = parser.parse_args()

    config_path = args.config
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    queue_client = QueueClient()
    upscale_client = UpscaleClient(config['imageUpscaleApiUrl'],
                                   config['imageUpscaleApiKey'])
    image_service = ImageServiceClient()

    image_processor = ImageProcessor(queue_client, upscale_client, image_service)

    results = image_processor.process_queue()
    total_processed = results.num_failure + results.num_success
    logger.info('Finished processing queue. Processed: {} Success: {} Failure: {}'.format(
        total_processed,
        results.num_success,
        results.num_failure))


if __name__ == "__main__":
    main()
