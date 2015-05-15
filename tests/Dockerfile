FROM centos:latest
MAINTAINER ckannan@iix.net
WORKDIR .
ADD *.rpm /
RUN yum -y swap -- remove centos-release* -- install /cloudrouter-release-centos*.rpm
RUN rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-*
RUN yum clean all
