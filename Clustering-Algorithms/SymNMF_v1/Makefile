# Makefile for compiling and linking the symnmf program

# Compiler and flags
COMPILER = gcc
FLAGS = -ansi -Wall -Wextra -Werror -pedantic-errors

# Source files
SRCS = symnmf.c

# Executable, object files and headers
EXECUTABLE = symnmf
OBJ_FILE = $(SRCS:.c=.o)
HEADERS = symnmf.h

# Default target
$(EXECUTABLE): $(OBJ_FILE) $(HEADERS)
	@echo "Linking $(EXECUTABLE) executable"
	@$(COMPILER) -o $(EXECUTABLE) $(OBJ_FILE) -lm

# Compile source file to object file
$(OBJ_FILE): symnmf.c 
	@echo "Compiling $(OBJ_FILE) to $(OBJ_FILE)"
	@$(COMPILER) $(FLAGS) -c symnmf.c 

clean:
	@echo "Cleaning up"
	@rm -f $(OBJ_FILE) $(EXECUTABLE)

# Phony targets
.PHONY: all clean
