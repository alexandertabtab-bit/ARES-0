# Data

This repository does not include private facility data or real industrial sensor records.

The dashboard currently uses **synthetic demonstration readings** generated in `simulation/factory_data.py`.

If real data is added later:
- document its source and license;
- remove personal or confidential facility information;
- keep raw data separate from processed data;
- never describe synthetic data as real measurements;
- split datasets by source/time where appropriate to avoid data leakage.

For YOLO training, create a separate labelled image dataset with documented usage rights and train/validation/test splits.
