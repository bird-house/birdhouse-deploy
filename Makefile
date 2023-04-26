# Generic variables
override SHELL       := bash
override APP_NAME    := birdhouse-deploy
override APP_VERSION := 1.26.0

# utility to remove comments after value of an option variable
override clean_opt = $(shell echo "$(1)" | $(_SED) -r -e "s/[ '$'\t'']+$$//g")

override _SED    := sed
override OS_NAME := $(uname)
ifeq ($(OS_NAME),Darwin)
  override _SED  := gsed
endif

# color codes and utility shortcuts
COLOR  ?= 1		## Enable or disable use of colors in outputs (eg: 'COLOR=0' will disable them)
COLOR  := $(call clean_opt,$(COLOR))
override ECHO   := echo
# all colors are undefined by default
# only define items that have actual text on top of colors
override _ERROR := "ERROR: "
override _WARN  := "WARN:  "
override _INFO  := "INFO:  "
override _DEBUG := "DEBUG: "
override _MAKE  := "make"
override _CONDA := "conda"
override _NA    := "\<n/a\>"
ifneq ("$(COLOR)", "0")
  # must make sure that interpretation of backslash escapes is enabled (not default for all terminals)
  # must use the full path otherwise make confuses it with its own echo command
  # reference: https://misc.flogisoft.com/bash/tip_colors_and_formatting
  override ECHO             := /bin/echo -e
  override _ESC             := $(shell printf '\033')
  override _NORMAL          := $(_ESC)[0m
  override _RED             := $(_ESC)[31m
  override _GREEN           := $(_ESC)[32m
  override _YELLOW          := $(_ESC)[33m
  override _BLUE            := $(_ESC)[34m
  override _MAGENTA         := $(_ESC)[35m
  override _CYAN            := $(_ESC)[36m
  override _DARK_GRAY       := $(_ESC)[90m
  override _LIGHT_CYAN      := $(_ESC)[96m
  override _BG_GRAY         := $(_ESC)[100m
  override _BG_DARK_RED     := $(_ESC)[48;5;52m
  override _BG_PURPLE       := $(_ESC)[48;5;55m
  override _BG_LIGHT_PURPLE := $(_ESC)[48;5;60m
  override _ORANGE          := $(_ESC)[38;5;166m
  override _LIGHT_ORANGE    := $(_ESC)[38;5;214m
  # concepts
  override _ERROR           := "$(_RED)$(_ERROR)$(_NORMAL)"
  override _WARN            := "$(_YELLOW)$(_WARN)$(_NORMAL)"
  override _INFO            := "$(_BLUE)$(_INFO)$(_NORMAL)"
  override _DEBUG           := "$(_DARK_GRAY)$(_DEBUG)$(_NORMAL)"
  override _CMD             := $(_ORANGE)
  override _MAKE            := $(_CMD)$(_MAKE)$(_NORMAL)
  override _CONDA           := $(_CMD)$(_CONDA)$(_NORMAL)
  override _NA              := $(_YELLOW)$(_NA)$(_NORMAL)
  override _FILE            := $(_LIGHT_CYAN)
  override _HEADER          := $(_BG_DARK_RED)
  override _EXTENSION       := $(_LIGHT_CYAN)
  override _UNKNOWN         := $(_LIGHT_ORANGE)
  override _SECTION         := $(_BG_GRAY)
  override _TARGET          := $(_CYAN)
  override _OPTION          := $(_MAGENTA)
  override _CONFIG          := $(_GREEN)
endif
override MSG_D := $(ECHO) $(_DEBUG)
override MSG_I := $(ECHO) $(_INFO)
override MSG_W := $(ECHO) $(_WARN)
override MSG_E := $(ECHO) $(_ERROR)

override TARGET_SIZE := 16
override OPTION_SIZE = 16
override OPTION_OFFSET = $(shell echo $$(($(OPTION_SIZE) + 3)))

CONDA_CMD ?=	## Conda command to execute prior to Python calls (can be used to activate environment if desired)
CONDA_CMD := $(call clean_opt,$(CONDA_CMD))

### Information Targets ###

.DEFAULT_GOAL := help

.PHONY: help
help:		## Display usage message
	@$(ECHO) "$(_HEADER)=== Makefile Help ===$(_NORMAL)\n"
	@$(MSG_I) "For available target commands, call the following:\n"
	@$(ECHO) "    $(_MAKE) $(_TARGET)targets$(_NORMAL)\n"
	@$(MSG_I) "For available options, call the following:\n"
	@$(ECHO) "    $(_MAKE) $(_OPTION)options$(_NORMAL)\n"

.PHONY: options
options:     ## Display configurable option details for execution of targets
	@$(ECHO) "$(_HEADER)=== Configurable Options [$(APP_NAME)] ===$(_NORMAL)\n"
	@$(MSG_I) "Use '$(_MAKE) $(_OPTION)OPTION$(_NORMAL)=<value> <$(_TARGET)target$(_NORMAL)>' \
		where <$(_OPTION)OPTION$(_NORMAL)> is one amongst below choices:\n"
	@grep -E '^\s*[a-zA-Z0-9_]+\s+\?\=.*$$' Makefile \
		| $(_SED) -r -e 's/\s*(.*)\s*\?\=[\s\t]*([^#]*[^#\s\t]+)?[\s\t]*(##\s+(.*))*$$/\1!!!\2!!!\3!!!\4/g' \
		| awk ' BEGIN {FS = "!!!"}; { \
			printf "  $(_TARGET)%-$(OPTION_SIZE)s$(_NORMAL)%s%-$(OPTION_OFFSET)s[default:%s]\n", $$1, $$4, "\n", $$2 \
		}'

.PHONY: targets
targets:	## Display available targets and descriptions
	@$(ECHO) "$(_HEADER)=== Makefile Targets [$(APP_NAME)] ===$(_NORMAL)\n"
	@grep -v -E '.*(\?|\:\=).*$$' Makefile | grep -E '\#\#.*$$' \
		| $(_SED) -r -e 's/([\sA-Za-z0-9\_\-]+)\:[\sA-Za-z0-9\_\-\.]+\s*\#{2,3}\s*(.*)\s*$$/\1!!!\2/g' \
		| awk ' BEGIN {FS = "(:|###)+.*?## "}; \
			/\#\#\#/ 	{printf "$(_SECTION)%s$(_NORMAL)\n", $$1;} \
			/:/   	 	{printf "  $(_TARGET)%-$(TARGET_SIZE)s$(_NORMAL) %s\n", $$1, $$2;} \
		  '
	@$(ECHO) ""

### Versioning Targets ###

# Bumpversion 'dry' config
# if 'dry' is specified as target, any bumpversion call using 'BUMP_XARGS' will not apply changes
BUMP_XARGS ?= --verbose --allow-dirty	## Extra arguments to pass down to version control utility
BUMP_XARGS := $(call clean_opt,$(BUMP_XARGS))
ifeq ($(filter dry, $(MAKECMDGOALS)), dry)
  BUMP_XARGS := $(BUMP_XARGS) --dry-run
endif
BUMP_CFG  ?= .bumpversion.cfg				## Bump version configuration (default recommended)
BUMP_CFG  := $(call clean_opt,$(BUMP_CFG))
BUMP_TOOL := bump2version
BUMP_PATH := $(CONDA_ENV_PATH)/bin/$(BUMP_TOOL)
BUMP_CMD  := $(BUMP_TOOL) --config-file "$(BUMP_CFG)"

# guess the applicable semantic level update if provided via major|minor|patch targets
# perform validation to avoid many combination provided simultaneously
override BUMP_VERSION_INPUT := 1
override BUMP_VERSION_LEVEL :=
ifeq ($(filter major, $(MAKECMDGOALS)), major)
  ifeq ($(BUMP_VERSION_LEVEL),)
    override BUMP_VERSION_LEVEL := major
    override BUMP_VERSION_INPUT := 0
  else
    $(error "Cannot combine 'major|minor|patch' simultaneously!")
  endif
endif
ifeq ($(filter minor, $(MAKECMDGOALS)), minor)
  ifeq ($(BUMP_VERSION_LEVEL),)
    override BUMP_VERSION_LEVEL := minor
    override BUMP_VERSION_INPUT := 0
  else
    $(error "Cannot combine 'major|minor|patch' simultaneously!")
  endif
endif
ifeq ($(filter patch, $(MAKECMDGOALS)), patch)
  ifeq ($(BUMP_VERSION_LEVEL),)
    override BUMP_VERSION_LEVEL := patch
    override BUMP_VERSION_INPUT := 0
  else
    $(error "Cannot combine 'major|minor|patch' simultaneously!")
  endif
endif
ifneq ($(VERSION),)
  ifneq ($(BUMP_VERSION_LEVEL),)
    $(error "Cannot combine 'major|minor|patch' simultaneously with explicit VERSION input!")
  endif
endif
# when none was provided, use patch to directly apply the explicit 'VERSION' specified as input
ifeq ($(BUMP_VERSION_LEVEL),)
  override BUMP_VERSION_LEVEL := --new-version "$(VERSION)" patch
endif

.PHONY: dry
dry: $(BUMP_CFG)	## Run 'bump' without applying changes (dry-run) (call: make VERSION=<MAJOR.MINOR.PATCH> bump dry)
	@-$(ECHO) > /dev/null

.PHONY: patch
patch: $(BUMP_CFG)	## Run 'bump' with automatic semantic versioning of the next PATCH number (call: make bump patch)
	@-$(ECHO) > /dev/null

.PHONY: minor
minor: $(BUMP_CFG)	## Run 'bump' with automatic semantic versioning of the next MINOR number (call: make bump minor)
	@-$(ECHO) > /dev/null

.PHONY: major
major: $(BUMP_CFG)	## Run 'bump' with automatic semantic versioning of the next MAJOR number (call: make bump major)
	@-$(ECHO) > /dev/null

# run bumpversion with replacement of the release time value within its config for auto-update on future revisions
.PHONY: bump
bump: bump-check bump-install  ## Bump version using specified <VERSION> (call: make VERSION=<MAJOR.MINOR.PATCH> bump)
	@-$(MSG_I) "Updating package version..."
	@[ $(BUMP_VERSION_INPUT) -eq 0 ] || [ "${VERSION}" ] || ( \
		$(MSG_E) "Argument 'VERSION' is not specified to bump version"; exit 1 \
	)
	@$(SHELL) -c ' \
		PRE_RELEASE_TIME=$$(head -n 1 RELEASE.txt | cut -d " " -f 2) && \
		$(CONDA_CMD) $(BUMP_CMD) $(BUMP_XARGS) $(BUMP_VERSION_LEVEL) && \
		POST_RELEASE_TIME=$$(head -n 1 RELEASE.txt | cut -d " " -f 2) && \
		echo "Replace $${PRE_RELEASE_TIME} → $${POST_RELEASE_TIME}" && \
		$(_SED) -i "s/$${PRE_RELEASE_TIME}/$${POST_RELEASE_TIME}/g" $(BUMP_CFG) && \
		git add $(BUMP_CFG) && \
		git commit --amend --no-edit \
	'

.PHONY: bump-install
bump-install:   ## Installs bumpversion if not detected in the environment
	@-$(SHELL) -c '$(CONDA_CMD) test -f "$(BUMP_PATH)" || pip install $(PIP_XARGS) $(BUMP_TOOL)'

.PHONY: bump-check
bump-check:		## Verifies that required bumpversion files are found
	@[ -f "$(BUMP_CFG)" ] || ( \
		$(MSG_E) "Missing required file [$(BUMP_CFG)]. Run [make init-bump] or update BUMP_CFG accordingly."; \
		exit 1 \
	);

.PHONY: version
version:	## Display project version
	@-$(MSG_I) "$(APP_NAME) version: $(APP_VERSION)"

### Execution Targets ###

SCRIPT ?= birdhouse/pavics-compose.sh	## Script to run the stack
SCRIPT := $(call clean_opt,$(SCRIPT))

.PHONY: start
start:		## Start the stack with current env.local definitions
	@-$(MSG_I) "Starting $(APP_NAME) stack..."
	@$(SHELL) $(SCRIPT) up -d

.PHONY: stop
stop:		## Stop the running stack
	@-$(MSG_I) "Stopping $(APP_NAME) stack..."
	@$(SHELL) $(SCRIPT) stop
