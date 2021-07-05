#!/bin/dash

pip install -e /openedx/requirements/eolquestion

cd /openedx/requirements/eolquestion
cp /openedx/edx-platform/setup.cfg .
mkdir test_root
cd test_root/
ln -s /openedx/staticfiles .

cd /openedx/requirements/eolquestion

DJANGO_SETTINGS_MODULE=lms.envs.test EDXAPP_TEST_MONGO_HOST=mongodb pytest eolquestion/tests.py

rm -rf test_root
