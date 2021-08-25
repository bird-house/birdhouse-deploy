ARG WEAVER_VERSION=latest

# make 'dockerize' binary available
#FROM jwilder/dockerize AS dockerize
#see:
#   https://github.com/jwilder/dockerize/issues/97
#   https://github.com/jwilder/dockerize/pull/132
FROM korbin/dockerize:latest AS dockerize

# move over binary and run normal weaver command
FROM pavics/weaver:${WEAVER_VERSION}-manager
COPY --from=dockerize /usr/local/bin/dockerize /usr/local/bin/dockerize
