# Firefly III Docker image

[![Packagist](https://img.shields.io/packagist/v/grumpydictator/firefly-iii.svg?style=flat-square)](https://packagist.org/packages/grumpydictator/firefly-iii) 
[![License](https://img.shields.io/github/license/firefly-iii/firefly-iii.svg?style=flat-square])](https://www.gnu.org/licenses/agpl-3.0.html) 
[![Donate using GitHub](https://img.shields.io/badge/donate-GitHub-green?logo=github&style=flat-square)](https://github.com/sponsors/JC5)
[![Docker Stars](https://img.shields.io/docker/stars/fireflyiii/core?style=flat-square)](https://hub.docker.com/r/fireflyiii/core)
[![Docker Pulls](https://img.shields.io/docker/pulls/fireflyiii/core?style=flat-square)](https://hub.docker.com/r/fireflyiii/core)

This repository contains some of the helper scripts you may need when setting up Firefly III using Docker.

## Docker image

The Firefly III Docker image is built [on Azure](https://dev.azure.com/Firefly-III/MainImage/_wiki/wikis/MainImage.wiki/3/Home) and published [on Docker Hub](https://hub.docker.com/r/fireflyiii/core). There are several tags available:

* `fireflyiii/core:latest`  
  The latest version. Will be stable.
* `fireflyiii/core:version-x.x.x`  
  A version tag, frozen to a specific version. Old version tags will be removed after about 6 months.

For daredevils, the following tags are available:

* `fireflyiii/core:develop`  
  The latest development build. May not even boot.
* `fireflyiii/core:alpha`  
  The latest alpha release, if available.
* `fireflyiii/core:beta`.  
  The latest beta release, if available.

## docker-compose.yml

This repository also contains the [docker-compose.yml](docker-compose.yml) file which you can use to instantly run a version of Firefly III with a MariaDB (aka MySQL) database.

Some people use another database image instead of the provided database. This is entirely up to you of course, but make sure you change the environment variables if you switch away from MySQL or MariaDB.

### Docker and system architectures

The [database image](https://hub.docker.com/_/mariadb) provided by [docker-compose.yml](docker-compose.yml) may not provide the same system architectures as the [Firefly III image](https://hub.docker.com/r/fireflyiii/core/tags?page=1&ordering=last_updated&name=latest) does. On system with a i386-architecture for example this means that Firefly III will run fine, but the provided database will not. Be aware that this may happen to you, although it's a rare occurence.

## Dockerfile

The Dockerfile no longer resides in this repository. The Dockerfile and the associated build script can be found [on Azure](https://dev.azure.com/Firefly-III/MainImage/_wiki/wikis/MainImage.wiki/3/Home). Please refer to the repository and the scripts over there.

Here are some links for your reading pleasure.

- [Firefly III on GitHub](https://github.com/firefly-iii/firefly-iii)
- [Firefly III Documentation](https://docs.firefly-iii.org/)
- [Firefly III on Docker Hub](https://hub.docker.com/r/fireflyiii/core)
- [Firefly III Docker on Azure](https://dev.azure.com/Firefly-III/MainImage)

Please open any issues you have [in the main repository](https://github.com/firefly-iii/firefly-iii).
