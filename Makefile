all: test integration-test package

test:
	tox -e py34-unittests
	tox -e py34-pkgpanda

integration-test:
	tox -e py34-pkgpanda-integration

package:
	bin/package.sh

deploy:
	bin/deploy.sh

code-quality:
	bin/code-quality.sh
