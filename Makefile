# CPSC 474 Final Project - Mini Pokémon Battle with MCTS Enhancements
# Group: Yejun Yun (RAVE) and William Zhong (Value Network)

.PHONY: test clean help full-benchmark play test-rave test-valuenet

# Default target: run quick test (tests all agents)
test:
	@echo "Testing: Greedy, MCTS, RAVE, Value Network..."
	python3 test.py

# Run full baseline benchmark
full-benchmark:
	@echo "Running full baseline MCTS benchmark (50 games)..."
	python3 benchmark_v2.py

# Test RAVE
test-rave:
	@echo "Testing RAVE..."
	cd yejun-rave && python3 benchmark_rave.py

# Test Value Network (requires numpy)
test-valuenet:
	@echo "Testing Value Network..."
	cd william-valuenetwork && python3 benchmark_value_net.py

# Play the game interactively
play:
	@echo "Starting interactive game..."
	python3 main_v2.py

# Clean generated files
clean:
	rm -rf __pycache__
	rm -f *.pyc
	rm -rf william-valuenetwork/__pycache__
	rm -f william-valuenetwork/*.pyc
	rm -rf yejun-rave/__pycache__
	rm -f yejun-rave/*.pyc
	@echo "Cleaned build artifacts"

# Help menu
help:
	@echo "Mini Pokémon Battle - MCTS Enhancements Project"
	@echo "Group: Yejun Yun (RAVE) and William Zhong (Value Network)"
	@echo ""
	@echo "Available targets:"
	@echo "  make test            - Run quick test, tests all"
	@echo "  make full-benchmark  - Run full baseline benchmark"
	@echo "  make test-rave       - Run RAVE benchmark"
	@echo "  make test-valuenet   - Run Value Network benchmark (requires numpy)"
	@echo "  make play            - Play the game interactively"
	@echo "  make clean           - Remove build artifacts"
	@echo "  make help            - Show this help message"
	@echo ""
	@echo "Main Files:"
	@echo "  test.py          - Quick test: Greedy, MCTS, RAVE, Value Network"
	@echo "  benchmark_v2.py  - Full baseline MCTS benchmark (50 games)"
	@echo "  battle_v2.py     - Game engine"
	@echo "  mcts_v2.py       - Standard MCTS with random rollouts"
	@echo ""
	@echo "Enhancements:"
	@echo "  yejun-rave/          - RAVE (Rapid Action Value Estimation)"
	@echo "  william-valuenetwork/ - AlphaGo-style value network (requires numpy)"

