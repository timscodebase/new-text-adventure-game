#!/usr/bin/env python3
"""AI Test Runner for the text adventure game."""

import argparse
import logging
import json
import sys
from datetime import datetime
from pathlib import Path

from game.engine import GameEngine
from game.ai_player import AIPlayer, AIStrategy


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('ai_test.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def run_single_test(strategy: AIStrategy, max_actions: int = 100, 
                   delay: float = 0.1, verbose: bool = True) -> dict:
    """Run a single AI test session."""
    print(f"\n🚀 Starting AI test with strategy: {strategy.value}")
    print(f"Max actions: {max_actions}, Delay: {delay}s")
    
    # Create game engine
    engine = GameEngine()
    
    # Create AI player
    ai_player = AIPlayer(strategy=strategy, max_actions=max_actions)
    
    # Run the test
    stats = ai_player.play_game(engine, delay=delay, verbose=verbose)
    
    # Save detailed log
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"ai_log_{strategy.value}_{timestamp}.txt"
    ai_player.save_log(log_filename)
    
    stats['log_file'] = log_filename
    stats['timestamp'] = timestamp
    
    return stats


def run_comprehensive_test(max_actions: int = 50, delay: float = 0.1) -> dict:
    """Run comprehensive tests with all strategies."""
    print("\n🧪 Running comprehensive AI testing suite...")
    
    all_results = {}
    
    for strategy in AIStrategy:
        print(f"\n{'='*50}")
        print(f"Testing Strategy: {strategy.value.upper()}")
        print(f"{'='*50}")
        
        try:
            stats = run_single_test(strategy, max_actions, delay, verbose=False)
            all_results[strategy.value] = stats
            
            # Print brief summary
            print(f"✅ {strategy.value}: {stats['success_rate']}% success, "
                  f"{stats['rooms_visited']} rooms, Level {stats['final_level']}")
            
        except Exception as e:
            print(f"❌ {strategy.value}: Failed with error: {e}")
            all_results[strategy.value] = {"error": str(e)}
    
    return all_results


def run_stress_test(strategy: AIStrategy = AIStrategy.RANDOM, 
                   iterations: int = 10, max_actions: int = 20) -> dict:
    """Run stress test with multiple iterations."""
    print(f"\n💪 Running stress test: {iterations} iterations of {strategy.value}")
    
    results = []
    failures = 0
    
    for i in range(iterations):
        print(f"\nIteration {i+1}/{iterations}")
        try:
            stats = run_single_test(strategy, max_actions, delay=0.01, verbose=False)
            results.append(stats)
            print(f"  ✅ Success rate: {stats['success_rate']}%")
        except Exception as e:
            failures += 1
            print(f"  ❌ Failed: {e}")
    
    # Calculate aggregate statistics
    if results:
        avg_success_rate = sum(r['success_rate'] for r in results) / len(results)
        avg_rooms = sum(r['rooms_visited'] for r in results) / len(results)
        avg_level = sum(r['final_level'] for r in results) / len(results)
        
        aggregate_stats = {
            "iterations": iterations,
            "successful_runs": len(results),
            "failed_runs": failures,
            "average_success_rate": round(avg_success_rate, 1),
            "average_rooms_visited": round(avg_rooms, 1),
            "average_final_level": round(avg_level, 1),
            "individual_results": results
        }
    else:
        aggregate_stats = {
            "iterations": iterations,
            "successful_runs": 0,
            "failed_runs": failures,
            "error": "All iterations failed"
        }
    
    return aggregate_stats


def save_results(results: dict, filename: str = None) -> str:
    """Save test results to JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_test_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {filename}")
    return filename


def print_comparison(results: dict) -> None:
    """Print a comparison of different strategies."""
    if not results:
        return
    
    print("\n📊 STRATEGY COMPARISON")
    print("="*70)
    print(f"{'Strategy':<12} {'Success%':<8} {'Rooms':<6} {'Level':<6} {'Gold':<6} {'Quests':<7}")
    print("-"*70)
    
    for strategy, stats in results.items():
        if 'error' in stats:
            print(f"{strategy:<12} {'ERROR':<8} {'-':<6} {'-':<6} {'-':<6} {'-':<7}")
        else:
            print(f"{stats.get('strategy', strategy):<12} "
                  f"{stats.get('success_rate', 0):<8} "
                  f"{stats.get('rooms_visited', 0):<6} "
                  f"{stats.get('final_level', 0):<6} "
                  f"{stats.get('final_gold', 0):<6} "
                  f"{stats.get('quests_completed', 0):<7}")
    
    print("="*70)


def main():
    """Main function to run AI tests."""
    parser = argparse.ArgumentParser(description="AI Test Runner for Text Adventure Game")
    parser.add_argument('--strategy', type=str, choices=[s.value for s in AIStrategy],
                       help='AI strategy to test')
    parser.add_argument('--max-actions', type=int, default=100,
                       help='Maximum actions per test (default: 100)')
    parser.add_argument('--delay', type=float, default=0.1,
                       help='Delay between actions in seconds (default: 0.1)')
    parser.add_argument('--comprehensive', action='store_true',
                       help='Run comprehensive test with all strategies')
    parser.add_argument('--stress-test', action='store_true',
                       help='Run stress test with multiple iterations')
    parser.add_argument('--iterations', type=int, default=10,
                       help='Number of iterations for stress test (default: 10)')
    parser.add_argument('--output', type=str,
                       help='Output file for results (default: auto-generated)')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--quiet', action='store_true',
                       help='Minimal output (overrides verbose)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose and not args.quiet)
    
    print("🎮 Text Adventure Game - AI Test Runner")
    print("="*50)
    
    results = {}
    
    try:
        if args.comprehensive:
            # Run comprehensive test
            results = run_comprehensive_test(args.max_actions, args.delay)
            print_comparison(results)
            
        elif args.stress_test:
            # Run stress test
            strategy = AIStrategy(args.strategy) if args.strategy else AIStrategy.RANDOM
            results = run_stress_test(strategy, args.iterations, args.max_actions)
            
            print(f"\n📈 STRESS TEST RESULTS")
            print(f"Strategy: {strategy.value}")
            print(f"Successful runs: {results['successful_runs']}/{results['iterations']}")
            if 'average_success_rate' in results:
                print(f"Average success rate: {results['average_success_rate']}%")
                print(f"Average rooms visited: {results['average_rooms_visited']}")
                print(f"Average final level: {results['average_final_level']}")
            
        elif args.strategy:
            # Run single strategy test
            strategy = AIStrategy(args.strategy)
            results = run_single_test(strategy, args.max_actions, args.delay, not args.quiet)
            
        else:
            # Default: run a quick test with explorer strategy
            print("No specific test specified, running default explorer test...")
            results = run_single_test(AIStrategy.EXPLORER, args.max_actions, args.delay, not args.quiet)
        
        # Save results
        if results:
            filename = save_results(results, args.output)
            print(f"\n✅ Testing completed successfully!")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        logging.error(f"Testing failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
