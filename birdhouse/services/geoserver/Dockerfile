# Temp fix to avoid altering docker image on startup, which makes the image not reproducible.
# docker build -t pavics/geoserver:2.19.0-kartoza-build20210329-r2-with-snakeyaml .

FROM pavics/geoserver:2.19.0-kartoza-build20210329

# Add missing jar for the metadata-plugin.
# Should be fixed by newer version of Geoserver and matching new version of the plugin.
# https://osgeo-org.atlassian.net/browse/GEOS-10078
RUN wget https://repo1.maven.org/maven2/org/yaml/snakeyaml/1.30/snakeyaml-1.30.jar \
    -O /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/snakeyaml-1.30.jar
