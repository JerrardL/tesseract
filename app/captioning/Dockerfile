#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

FROM nvidia/cuda:11.0.3-cudnn8-devel-ubuntu20.04

ADD ./requirements.txt /requirements.txt
RUN apt-get update \
&& apt-get install python3 -y
RUN apt-get install python3-pip -y

RUN pip3 install --upgrade pip \
&& pip3 install -r /requirements.txt \
&& DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y ffmpeg

WORKDIR /app

COPY . /app

CMD python3 app.py
