# Makefile

help:
	@echo
	@echo "  BoxWorks 2020 Portal Makefile"
	@echo "  -----------------------------------------------------------------------------------------------------------"
	@echo "  dev                       to build the development Docker image"

dev:
	docker-compose -f docker-compose.yml down
	docker-compose docker-compose.yml up
