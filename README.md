This repo contains notebooks for fine-tuning YAMNet (https://github.com/tensorflow/models/tree/master/research/audioset/yamnet).

- `generate YAMNet input.ipynb` pre-computes spectrograms from audio files and stores them as `.npy` these are then loaded during training using a custom Tensorflow data generator defined in `datagen_yamnet.py`. Pre-computing the spectrograms greatly increases the speed of training / experimentation.

- `fine-tune YAMNet.ipynb` sets up spectrogram data generators, loads AudioSet weights into YAMNet and adds a custom network top, and runs transfer learning and fine-tuning.

##### References

* https://github.com/tensorflow/models/tree/master/research/audioset/yamnet

* Gemmeke, J. et. al.,
  [AudioSet: An ontology and human-labelled dataset for audio events](https://research.google.com/pubs/pub45857.html),
  ICASSP 2017

* Hershey, S. et. al.,
  [CNN Architectures for Large-Scale Audio Classification](https://research.google.com/pubs/pub45611.html),
  ICASSP 2017