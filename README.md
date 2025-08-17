# Compiler Design Project

## Overview
This repository contains the semester-long project for **CSE304 – Compiler Design**.  
The project walks step by step through the construction of a simple compiler, starting from the **lexical analyzer** and ending with a working **compiler** that ties all phases together.  
Each folder contains, Dockerfile, which enables users to test and run the program without the need to install any applications. There is a guide **dockerStart.txt** which gives 
sufficient information to run the program

The purpose of this project is to gain hands-on experience in the design and implementation of compiler components and to understand how source code is transformed into executable code.


---

## Project Structure
The project is organized into multiple **phases**, each representing a key milestone in compiler development:

- **Phase 1: Lexical Analyzer**
  - Implementation of a scanner to tokenize the input program.
  - Handles identifiers, keywords, operators, and error detection.

- **Phase 2: Symbol Table Management**
  - Data structures for maintaining symbols, their scope, and attributes.
  - Supports insertion, lookup, and management of identifiers.

- **Phase 3: Parser & Lexer Integration**
  - Construction of a parser to recognize the grammar of the language.
  - Integration of the lexer with the parser to process source code into syntax trees.
  - Includes test cases for control flow, expressions, and error handling.

- **Phase 4: Compiler Integration**
  - Brings together the lexer, parser, and symbol table into a full compiler pipeline.
  - Demonstrates the end-to-end compilation of a simple language.
  - Includes extended test cases for arrays, loops, I/O, and functions.

---

## Repository Layout
  - phase1/ → Lexical analyzer
  - phase2/ → Symbol table management
  - phase3/ → Parser & test cases
  - phase4/ → Complete compiler (lexer + parser + symbol table)
