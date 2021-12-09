#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info(f"Donwloading data: {args.input_artifact}")
    local_path = wandb.use_artifact(args.input_artifact).file()
    logger.info(f"Data was saved in {local_path}")
    df = pd.read_csv(local_path)
    
    logger.info("Drop outliers")
    logger.info(f"Clipping prices from {args.min_price} to {args.max_price}")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    
    logger.info("Drop outside area")
    idx = df['longitude'].between(-74.25, -
                                  73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    
    logging.info("Convert last_review to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    logger.info(f"Saving results as {args.output_artifact}")
    df.to_csv(args.output_artifact, index=False)
    
    logger.info("Logging artifact in W&B")
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description
     )
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)
    
    run.finish()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="input artifact name",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="output artifact name",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="output type og the artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Output description of the artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Min price allowed for clipping outliers",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Max price allowed for clipping outliers",
        required=True
    )


    args = parser.parse_args()

    go(args)
