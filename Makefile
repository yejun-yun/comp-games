# CPSC 474 Final Project - Mini Pokémon Battle with MCTS
# William Zhong

.PHONY: test clean help full-benchmark play

# Default target: run quick test
test:
	@echo "Running quick test suite (2-3 minutes)..."
	python3 test.py

# Run full benchmark (5-10 minutes)
full-benchmark:
	@echo "Running full benchmark suite..."
	python3 benchmark_v2.py

# Play the game interactively
play:
	@echo "Starting interactive game..."
	python3 main_v2.py

# Clean generated files
clean:
	rm -rf __pycache__
	rm -f *.pyc
	rm -f william-valuenetwork/*.pyc
	rm -f william-valuenetwork/__pycache__
	@echo "Cleaned build artifacts"

# Help menu
help:
	@echo "Mini Pokémon Battle - MCTS Project"
	@echo ""
	@echo "Available targets:"
	@echo "  make test            - Run quick test suite (~2-3 min, 20 games per config)"
	@echo "  make full-benchmark  - Run full benchmark (~5-10 min, 50 games per config)"
	@echo "  make play            - Play the game interactively"
	@echo "  make clean           - Remove build artifacts"
	@echo "  make help            - Show this help message"
	@echo ""
	@echo "Files:"
	@echo "  test.py          - Quick test script with project description"
	@echo "  benchmark_v2.py  - Full benchmark (multiple simulation budgets)"
	@echo "  main_v2.py       - Interactive game with multiple modes"
	@echo "  mcts_v2.py       - MCTS implementation with random rollouts"
	@echo "  battle_v2.py     - Game engine"
	@echo ""
	@echo "Optional Enhancement:"
	@echo "  william-valuenetwork/  - AlphaGo-style value network (requires numpy)"

