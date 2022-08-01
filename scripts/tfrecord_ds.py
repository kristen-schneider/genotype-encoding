import basic_ds

import tensorflow as tf
import numpy as np
from itertools import zip_longest, takewhile
from joblib import Parallel, delayed

class DataWriter:
    def __init__(self, input_file, out_dir, training, num_classes=3):
        self.input_file = input_file
        self.out_dir = out_dir
        self.training = training
        self.num_classes = num_classes

    @staticmethod
    def _int64_feature(value):
        if not isinstance(value, list):
            value = [value]
        return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

    @staticmethod
    def _bytes_feature(value):
        # If the value is an eager tensor BytesList
        # won't unpack a string from an EagerTensor.
        if isinstance(value, tf.Tensor):
            value = value.numpy()
        elif not isinstance(value, bytes):
            value = value.encode()
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    @staticmethod
    def get_basic_dataset(input_file):
        """
        Builds a tensorflow dataset object from file with 3 columns:
        sample1, sample2, IBD_distance
        :param CNN_input_file:
        :return: tensorflow dataset object for input to cnn model
        """
        f = open(input_file, 'r')
        header = f.readline()
        sample1_data, sample2_data, distances_data = [], [], []
        for line in f:
            currS1, currS2 = [], []
            A = line.strip().split()

            for i in A[0]: currS1.append(int(i))
            sample1_data.append(currS1)

            for j in A[1]: currS2.append(int(j))
            sample2_data.append(currS1)

            distances_data.append(A[2])

        # each set of input data is its own tensor
        sample1_ds = tf.data.Dataset.from_tensor_slices(sample1_data)
        sample2_ds = tf.data.Dataset.from_tensor_slices(sample2_data)
        distances_ds = tf.data.Dataset.from_tensor_slices(distances_data)

        # map sample encodings to list of ints and distance values to float
        sample1_ds_float = sample1_ds.map(lambda x: int(x))
        sample2_ds_float = sample2_ds.map(lambda x: int(x))
        distances_ds_float = distances_ds.map(lambda x: float(x))

        # zip 3 tensor items together into one dataset
        full_ds = tf.data.Dataset.zip((sample1_ds_float, sample2_ds_float, distances_ds_float))
        # puts 1 element into a batch
        full_ds_batch = full_ds.batch(2)
        return full_ds_batch
        # return basic_ds.build_dataset_from_file(input_file)


    @staticmethod
    def _serialize_example(filename, label):
        """
        given a filepath to an image (label contained in filename),
        serialize the (image, label)
        """
        example = tf.train.Example(
            features=tf.train.Features(
                feature={
                    'filename': DataWriter._bytes_feature(filename),
                    'image': DataWriter._bytes_feature(
                        tf.io.serialize_tensor(DataWriter._load_image(filename))),
                    'label': DataWriter._int64_feature(label),
                }
            )
        )
        return example.SerializeToString()

    @staticmethod
    def _write_batch(out_dir, batch_index, file_label_pairs, training):
        """
        Write a single batch of images to TFRecord format
        """
        with tf.io.TFRecordWriter(
                f"{out_dir}/{training}/{training}_{batch_index:05d}.tfrec") as writer:
            for file_label in file_label_pairs:
                filename, label = file_label
                serialized_example = DataWriter._serialize_example(filename, label)
                writer.write(serialized_example)

    def to_tfrecords(self, imgs_per_record=1000):
        """
        Write train and/or val set to a set of TFRecords
        """
        Parallel(n_jobs=-1)(
            delayed(self._write_batch)(self.out_dir,
                                       batch_index=i,
                                       file_label_pairs=takewhile(
                                           lambda x: x is not None,
                                           file_label_pairs),
                                       training=self.training)
            for i, file_label_pairs in enumerate(
                DataWriter._grouper(zip(self.filenames, self.labels), imgs_per_record))
        )
#
#
# class DataReader:
#     def __init__(self,
#                  data_list,  # list of original images in the dataset
#                  tfrec_list,  # list of tfrecords in the dataset (s3 or local)
#                  num_processes,
#                  batch_size):
#         self.data_list = data_list
#         self.tfrec_list = tfrec_list
#         self.num_processes = num_processes
#         self.batch_size = batch_size
#
#     @staticmethod
#     def _parse_image(x):
#         """
#         Used to reformat serialzed images to original shape
#         """
#         result = tf.io.parse_tensor(x, out_type=tf.float32)
#         result = tf.reshape(result, IMAGE_SHAPE)
#         return result
#
#     @staticmethod
#     def _parse_serialized_example(serialized_example):
#         """
#         Given a serialized example with the below format, extract/deserialize
#         the image and (one-hot) label
#         """
#         features = {
#             'filename': tf.io.FixedLenFeature((), tf.string),
#             'image': tf.io.FixedLenFeature((), tf.string),
#             'label': tf.io.FixedLenFeature((), tf.int64)
#         }
#         example = tf.io.parse_single_example(serialized_example, features)
#
#         # read image and perform transormations
#         image = DataReader._parse_image(example['image'])
#         image = tf.image.per_image_standardization(image)
#
#         label = example['label']
#         return image, tf.one_hot(label, depth=3, dtype=tf.int64)
#
#     def get_dataset(self):
#         n_images = len(open(self.data_list).readlines())
#
#         # we don't need examples to be loaded in order (better speed)
#         options = tf.data.Options()
#         options.experimental_deterministic = False
#
#         with open(self.tfrec_list) as f:
#             files = [filename.rstrip() for filename in f]
#             dataset = tf.data.Dataset.from_tensor_slices(files) \
#                 .shuffle(len(files)) \
#                 .with_options(options)
#
#         dataset = dataset.interleave(
#             tf.data.TFRecordDataset,
#             cycle_length=self.num_processes,
#             num_parallel_calls=self.num_processes) \
#  \
#                 dataset = dataset.map(
#                     functools.partial(DataReader._parse_serialized_example),
#                     num_parallel_calls=self.num_processes) \
#                     .repeat() \
#                     .shuffle(buffer_size=1000) \
#                     .batch(self.batch_size, drop_remainder=False) \
#                     .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
#
#         return dataset, n_images