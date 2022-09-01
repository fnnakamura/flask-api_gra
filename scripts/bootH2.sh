#!/bin/sh

project_path=$(dirname $(dirname $(realpath $0)))

java -cp $project_path/infra/h2-2.1.212.jar org.h2.tools.Server -tcp -tcpAllowOthers -tcpPort 5234 -baseDir $project_path/infra/ -ifNotExists
