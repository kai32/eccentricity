import os
import stat

# SETTING
EXPERIMENT = 'demo-experiment'


os.makedirs('experiments/{}/gen/scripts'.format(EXPERIMENT), exist_ok=True)
os.makedirs('experiments/{}/gen/trainlogs'.format(EXPERIMENT), exist_ok=True)
os.makedirs('experiments/{}/gen/trained'.format(EXPERIMENT), exist_ok=True)

train_all_sh = os.path.join('experiments/{}/gen/scripts/train_all.sh'.format(EXPERIMENT))
with open(train_all_sh, 'w') as g:

  # SETTING Settings common to all models to train for this experiment:
  pm = '11-1-1-1-1'
  total_pool = True

  g.write('#!/bin/sh\n')
  # SETTING Settings to change among different models:
  for lr in [0.1, 0.01, 0.001]:
    for contrast_norm in ['areafactor',  'None']:

      # SETTING
      model_name = '{}_total_pool_contrast_{}_lr{}'.format(pm, contrast_norm, lr)

      # SETTING
      pycmd = ('src/python/ecc/ecc_train.py '
        '--parity=even '
        '--learning_rate={} '
        '--pm={} '
        '--model_name={} '
        '--total_pool={} '
        '--train_dir={} '
        '--num_scales={} '
        '--contrast_norm={} '
        '--random_shifts '.format(
          lr,
          pm,
          model_name,
          total_pool,
          os.path.join('experiments', EXPERIMENT, 'gen'),
          pm.split('-')[0], # num scales
          contrast_norm))
      logdir = 'experiments/{}/gen/trainlogs/{}.log '.format(EXPERIMENT, model_name)
      log= ' | tee {}'.format(logdir)
      shname = os.path.join('experiments/{}/gen/scripts'.format(EXPERIMENT), 'train_{}.sh'.format(model_name))
      with open(shname, 'w') as f:
        f.write('#!/bin/sh\n')
        f.write('unbuffer ' + pycmd + log)
      st = os.stat(shname)
      os.chmod(shname, st.st_mode | stat.S_IEXEC)

      g.write('echo running {}, logs written to {} \n'.format(model_name, logdir))
      g.write(shname + '\n')

st = os.stat(train_all_sh)
os.chmod(train_all_sh, st.st_mode | stat.S_IEXEC)
