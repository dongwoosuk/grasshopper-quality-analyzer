"""
Grasshopper Performance Profiler - v1.0

Real-time performance analysis and bottleneck identification for GH definitions

Measures component execution times and identifies performance bottlenecks

Inputs (from Grasshopper):
- path: Text - Path to standalone folder containing gh_live_analyzer.py
- mode: Integer - Profiling mode: 0=Quick (1 pass), 1=Detailed (5 passes), 2=Live (default: 0)
- threshold_ms: Number - Slow component threshold in milliseconds (default: 100)
- top_n: Integer - Show top N slowest components (default: 10)
- auto_select: Boolean - Automatically select slow components in canvas (default: False)
- run_profile: Boolean - Trigger profiling execution

Outputs:
- report: Performance analysis report with bottlenecks
- slow_components: List of slow component GUIDs (for highlighting)
- timing_data: Detailed timing data (DataTree)
- suggestions: Optimization suggestions
"""

import sys
import os

# === PATH INPUT VALIDATION ===
if 'path' not in dir() or not path:  # type: ignore
    report = """❌ PATH REQUIRED!

Please connect 'path' input with your standalone folder location.

Example:
1. Add text panel with: r"C:\\Users\\Soku\\OneDrive - Steinberg Hart\\Desktop\\Source\\RhinoScripts\\src\\gh\\gh_analyzer_release\\standalone"
2. Connect to 'path' input

Optional Inputs:
- mode (Integer): 0=Quick, 1=Detailed, 2=Live (default: 0)
- threshold_ms (Number): Slow threshold in ms (default: 100)
- top_n (Integer): Number of slowest to show (default: 10)
- auto_select (Boolean): Auto-select slow components (default: False)
- run_profile (Boolean): Trigger profiling (set to True)

💡 Set 'run_profile' to True to start performance analysis
"""
    slow_components = []
    timing_data = None
    suggestions = ""

elif not os.path.exists(str(path).strip()):  # type: ignore
    report = f"""❌ PATH NOT FOUND: {path}

Please check:
1. Path exists
2. Spelling is correct
3. Use raw string format: r"C:\\path\\to\\folder"
"""
    slow_components = []
    timing_data = None
    suggestions = ""

else:
    gh_path = str(path).strip()  # type: ignore
    analyzer_file = os.path.join(gh_path, 'gh_live_analyzer.py')

    if not os.path.exists(analyzer_file):
        report = f"""❌ gh_live_analyzer.py not found in: {gh_path}

Please ensure gh_live_analyzer.py exists in the specified folder.
"""
        slow_components = []
        timing_data = None
        suggestions = ""

    else:
        try:
            # Load the analyzer
            with open(analyzer_file, 'r', encoding='utf-8') as f:
                exec(f.read())

            # Get profiling parameters
            profile_mode = 0  # Default: quick
            try:
                if 'mode' in dir() and mode is not None:  # type: ignore
                    profile_mode = int(mode)  # type: ignore
                    if profile_mode not in [0, 1, 2]:
                        profile_mode = 0
            except:
                pass

            threshold = 100.0  # Default: 100ms
            try:
                if 'threshold_ms' in dir() and threshold_ms is not None:  # type: ignore
                    threshold = float(threshold_ms)  # type: ignore
                    if threshold <= 0:
                        threshold = 100.0
            except:
                pass

            top_count = 10  # Default: top 10
            try:
                if 'top_n' in dir() and top_n is not None:  # type: ignore
                    top_count = int(top_n)  # type: ignore
                    if top_count <= 0:
                        top_count = 10
            except:
                pass

            should_select = False  # Default: don't auto-select
            try:
                if 'auto_select' in dir() and auto_select:  # type: ignore
                    should_select = True
            except:
                pass

            should_run = False  # Default: don't run
            try:
                if 'run_profile' in dir() and run_profile:  # type: ignore
                    should_run = True
            except:
                pass

            # Run profiling if triggered
            if should_run:
                # Create analyzer
                analyzer = GHLiveAnalyzer()

                # Determine mode
                if profile_mode == 1:
                    mode_str = 'detailed'
                    iterations = 5
                elif profile_mode == 2:
                    mode_str = 'quick'  # Live mode uses quick profiling repeatedly
                    iterations = 1
                else:
                    mode_str = 'quick'
                    iterations = 1

                # Run profiling
                timing_result = analyzer.profile_document(mode=mode_str, iterations=iterations)

                if 'error' in timing_result:
                    report = f"""❌ PROFILING FAILED: {timing_result['error']}

This may be due to:
- Document access issues
- Component computation errors
- Grasshopper version compatibility

Try:
1. Ensure Grasshopper document is open and active
2. Check if definition has circular references
3. Verify all components are functioning properly
4. Try with a simpler mode (mode=0)
"""
                    slow_components = []
                    timing_data = None
                    suggestions = ""

                else:
                    # Generate report
                    report = analyzer.generate_performance_report(style='full')

                    # Get bottlenecks
                    bottlenecks = analyzer.find_performance_bottlenecks(
                        threshold_ms=threshold,
                        top_n=top_count
                    )

                    # Extract slow component GUIDs
                    slow_components = [b['guid'] for b in bottlenecks]

                    # Convert timing data to simple format
                    timing_data = []
                    for guid, data in timing_result.items():
                        timing_data.append({
                            'guid': guid,
                            'name': data['name'],
                            'avg_time_ms': data['avg_time_ms'],
                            'category': data['category'],
                            'type': data['type']
                        })

                    # Get optimization suggestions
                    opt_suggestions = analyzer.get_optimization_suggestions()

                    suggestion_lines = []
                    suggestion_lines.append("=" * 60)
                    suggestion_lines.append("OPTIMIZATION SUGGESTIONS")
                    suggestion_lines.append("=" * 60)
                    suggestion_lines.append("")

                    if opt_suggestions:
                        for i, sug in enumerate(opt_suggestions, 1):
                            suggestion_lines.append(f"{i}. {sug['component']}")
                            suggestion_lines.append(f"   Issue: {sug['issue']}")
                            suggestion_lines.append(f"   Suggestions:")
                            for s in sug.get('suggestions', []):
                                suggestion_lines.append(f"      • {s}")
                            suggestion_lines.append("")
                    else:
                        suggestion_lines.append("✅ No specific optimization suggestions")
                        suggestion_lines.append("   Your definition is performing well!")
                        suggestion_lines.append("")

                    suggestion_lines.append("=" * 60)
                    suggestions = '\n'.join(suggestion_lines)

                    # Auto-select slow components if requested
                    if should_select and bottlenecks:
                        selected_count = analyzer.highlight_slow_components(threshold_ms=threshold)
                        report += f"\n\n🎯 Auto-selected {selected_count} slow components in canvas"

                    # Add mode indicator
                    mode_names = {0: "QUICK", 1: "DETAILED", 2: "LIVE"}
                    mode_name = mode_names.get(profile_mode, "QUICK")

                    header = f"""🦗 GRASSHOPPER PERFORMANCE PROFILER
Mode: {mode_name} | Threshold: {threshold:.0f}ms | Top: {top_count}

"""
                    report = header + report

            else:
                # Not triggered - show instructions
                mode_names = {0: "Quick (1 pass)", 1: "Detailed (5 passes avg)", 2: "Live monitoring"}
                current_mode = 0
                try:
                    if 'mode' in dir() and mode is not None:  # type: ignore
                        current_mode = int(mode) if int(mode) in [0, 1, 2] else 0  # type: ignore
                except:
                    pass

                report = f"""⏸ PERFORMANCE PROFILER READY

Current Settings:
   Mode: {mode_names.get(current_mode, 'Quick (1 pass)')}
   Threshold: {threshold:.0f}ms
   Top N: {top_count}
   Auto-select: {'Yes' if should_select else 'No'}

📝 To start profiling:
   Set 'run_profile' input to True

💡 Tips:
   • Quick mode (0): Fast, single measurement
   • Detailed mode (1): More accurate, averages 5 passes
   • Live mode (2): For continuous monitoring
   • Threshold: Components slower than this will be highlighted
   • Auto-select: Automatically select slow components in canvas

🎯 Workflow:
   1. Set run_profile = True
   2. Review the performance report
   3. Check optimization suggestions
   4. Select slow components (if auto_select = True)
   5. Optimize identified bottlenecks
   6. Re-profile to measure improvement
"""
                slow_components = []
                timing_data = None
                suggestions = ""

        except Exception as e:
            report = f"""❌ PERFORMANCE PROFILER FAILED: {str(e)}

This may be due to:
- Document access issues
- Grasshopper version compatibility
- Analyzer engine problems

Debugging steps:
1. Test with Health Check component first
2. Ensure gh_live_analyzer.py is up to date
3. Check console for additional error messages
4. Try with a simpler definition first

If issue persists:
- Check that Grasshopper document is open
- Verify Python component has proper permissions
- Review error message above for specific details
"""
            slow_components = []
            timing_data = None
            suggestions = ""
