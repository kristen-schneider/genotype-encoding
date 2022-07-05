# genotype-encoding
1. Install [TensorFlow](https://www.tensorflow.org/install), [gdown](https://github.com/wkentaro/gdown), and [unzip](https://github.com/conda-forge/unzip-feedstock)
```
conda install -c conda-forge tensorflow
conda install -c conda-forge gdown
conda install unzip
```
2. Download and unzip the Totally Looks Like Data
```
gdown --id 1jvkbTr_giSP3Ru8OwGNCg6B4PvVbcO34
gdown --id 1EzBZUb_mh_Dp_FKD0P4XiYYSd0QBH5zW
unzip -oq left.zip -d ~/.keras
unzip -oq right.zip -d ~/.keras
```
3. Follow [Keras Siamese Network Script](https://github.com/keras-team/keras-io/blob/master/examples/vision/siamese_network.py)
