import basic_ds

import tensorflow as tf
from itertools import zip_longest, takewhile
from joblib import Parallel, delayed

import functools

class DataWriter:
    def __init__(self, sample_ID_file, sample_encoding_file, pairwise_IBD_file, out_dir):
        self.sample_ID_file = sample_ID_file
        self.sample_encoding_file = sample_encoding_file
        self.pairwise_IBD_file = pairwise_IBD_file
        self.out_dir = out_dir

    @staticmethod
    def _sample_encoding_dict(sample_ID_file, sample_encoding_file):
        """
        Creates a dictionary of sampleID: sample_encoding from two files

        :return: dictionary with key as sampleID and value as trivial encoding
        """
        ID_encoding_dict = dict()

        # create list of all sample IDs in order
        f_IDs = open(sample_ID_file, 'r')
        ID_list = [line.strip() for line in f_IDs]
        f_IDs.close()

        # opens encoding file and
        f_encodings = open(sample_encoding_file, 'r')
        sample_i = 0
        for line in f_encodings:
            sample_encoding = line.strip()
            ID_encoding_dict[ID_list[sample_i]] = sample_encoding
            sample_i += 1
        f_encodings.close()
        return ID_encoding_dict

    @staticmethod
    def _pair_IBD_tuple(pairwise_IBD_file):
        """
        Creates a list of tuples from IBD file

        :return: list of tuple with (sample1_ID, sample2_ID, distance)
        """
        pair_IBD_tuple = []

        # create tuple of all sample1, sample2, distance
        f_IBDs = open(pairwise_IBD_file, 'r')
        header = None
        for line in f_IBDs:
            if header == None: header = line
            else:
                A = line.strip().split()
                sample1_ID = A[1]
                sample2_ID = A[3]
                distance = float(A[11])
                tuple_line = tuple([sample1_ID, sample2_ID, distance])
                pair_IBD_tuple.append(tuple_line)
        f_IBDs.close()

        return pair_IBD_tuple

    @staticmethod
    def _grouper(iterable, n, fillvalue=None):
        """
        Collect data into fixed-length chunks or blocks,
        Taken from python itertools docs
        """
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    @staticmethod
    def _bytes_feature(value):
        """

        :param value: bytes
        :return: takes input value and serializes
        """
        if isinstance(value, tf.Tensor):
            value = value.numpy()
        elif not isinstance(value, bytes):
            value = value.encode()
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    @staticmethod
    def _int64_feature(value):
        """
        :param value: integer
        :return: takes input integer value and serializes
        """
        if not isinstance(value, list):
            value = [value]
        return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

    @staticmethod
    def _float_feature(value):
        """
        :param value: float
        :return: takes input float value and serializes
        """
        return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

    @staticmethod
    def _serialize_example(sample1, sample2, distance):
        """
        given an input tensor (s1, s2, distance), serialize the entire input
        """
        example = tf.train.Example(
            features=tf.train.Features(
                feature={
                    'sample1': DataWriter._bytes_feature(sample1),
                    'sample2': DataWriter._bytes_feature(sample2),
                    'distance': DataWriter._float_feature(distance),
                }
            )
        )
        return example.SerializeToString()

    @staticmethod
    def _write_batch(out_dir, batch_index, pairwiseIBD_batch, sample_encodings):
        """

        """
        with tf.io.TFRecordWriter(
                f"{out_dir}/_{batch_index:05d}.tfrec") as writer:
            for pair in pairwiseIBD_batch:
                s1_encoding = sample_encodings[pair[0]]
                s2_encoding = sample_encodings[pair[1]]
                distance = pair[2]
                serialized_example = DataWriter._serialize_example(s1_encoding, s2_encoding, distance)
                writer.write(serialized_example)

    def to_tfrecords(self):
        """
        1. Make ID_encoding dictionary
        2. Make pair_IBD tuple
        3. IN BATCHES:
            take sampleIDs in tuple, look up their encoding
            writing encoding + distance to tf record.

        """
        BATCH_SIZE = 5000
        ID_encoding_dict = self._sample_encoding_dict(self.sample_ID_file, self.sample_encoding_file)
        ALL_pairIBD_tuples = self._pair_IBD_tuple(self.pairwise_IBD_file)

        # for i, pairwiseIBD_batch in enumerate(
        #         DataWriter._grouper(ALL_pairIBD_tuples, BATCH_SIZE)):
        #     self._write_batch(self.out_dir,
        #                       batch_index=i,
        #                       pairwiseIBD_batch=takewhile(
        #                           lambda x: x is not None,
        #                           pairwiseIBD_batch),
        #                       sample_encodings=ID_encoding_dict)


        Parallel(n_jobs=-1)(
            delayed(self._write_batch)(self.out_dir,
                                       batch_index=i,
                                       pairwiseIBD_batch=takewhile(
                                           lambda x: x is not None,
                                           pairwiseIBD_batch),
                                       sample_encodings=ID_encoding_dict)
            for i, pairwiseIBD_batch in enumerate(
                DataWriter._grouper(ALL_pairIBD_tuples, BATCH_SIZE))
        )


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
#         dataset = tf.dataset.interleave(
#             tf.data.TFRecordDataset,
#             cycle_length=self.num_processes,
#             num_parallel_calls=self.num_processes) \
#  \
#                 dataset = tf.dataset.map(
#                     functools.partial(DataReader._parse_serialized_example),
#                     num_parallel_calls=self.num_processes) \
#                     .repeat() \
#                     .shuffle(buffer_size=1000) \
#                     .batch(self.batch_size, drop_remainder=False) \
#                     .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
#
#         return dataset, n_images
