DOC_FOLDERS := docs/html docs/latex
CPPS := $(shell ls src/*.cpp)
HPPS := $(shell ls src/*.hpp)
TEMP := $(subst src/,obj/,$(CPPS))
OBJS := $(subst .cpp,.o,$(TEMP))

MAVLINK_DIR := lib/mavlink/v1.0

INCLUDES := -isystem $(MAVLINK_DIR) 
LINKER_FLAGS := -pthread -lboost_system -lboost_log -lhackrf

CC := clang++ --std=c++14
CFLAGS := -Wall -Wpedantic -Werror -g

DATALOGGER := bin/datalogger

.PHONY: all clean docs format

all: $(DATALOGGER)

$(DATALOGGER): git_submodule $(OBJS)
	@mkdir -p bin/
	$(CC) $(OBJS) $(CFLAGS) -o $(DATALOGGER) $(LINKER_FLAGS) 

git_submodule:
	git submodule update --init --recursive

obj/%.o: src/%.cpp
	@mkdir -p obj/
	$(CC) $(CFLAGS) $(INCLUDES) -DBOOST_LOG_DYN_LINK -c $< -o $@

clean:
	rm -rf $(DOC_FOLDERS) obj/ bin/

docs:
	doxygen docs/Doxyfile

format:
	@for SRC in $(CPPS); do\
		echo "Formatting source $$SRC"; \
		clang-format -i $$SRC; \
	done
	@for HDR in $(HPPS); do\
		echo "Formatting header $$HDR"; \
		clang-format -i $$HDR;\
	done
	@echo "Done"
