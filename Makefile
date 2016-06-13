all: test integration-test package

test:
	tox -e py34-unittests
	tox -e py34-pkgpanda
	mkdir -p coverage-reports
	coverage combine .coverage_unittests .coverage_pkgpanda
	coverage xml -o coverage-reports/ut-coverage.xml
	mv .coverage coverage.ut

integration-test:
	tox -e py34-pkgpanda-integration
	mkdir -p coverage-reports
	coverage xml -o coverage-reports/it-coverage.xml
	mv .coverage coverage.it

package:
	bin/package.sh

deploy:
	bin/deploy.sh

code-quality:
	bin/code-quality.sh
