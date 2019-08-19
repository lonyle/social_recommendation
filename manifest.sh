### part 1: run the simulations in Section 6
python simulation/exp2.2_impact_initial_info_prob.py
python plot/plot2.2_impact_initial_info_prob.py

# python simulation/exp2.3_impact_rec_prob.py
# python plot/plot2.3_impact_rec_prob.py

# python simulation/exp2.4_impact_adopt_prob.py
# python plot/plot2.4_impact_adopt_prob.py

# python simulation/exp3_impact_perceivability.py
# python plot/plot3_perceivability.py

# python simulation/exp4_impact_social_value.py
# python plot/plot4_social_value.py

### part 2: run the optimizations in Section 7 (For facebook graph)
# python optimization/exp9.0_reward.py --graph_name Facebook
# python plot/plot9.0_reward.py

# python optimization/exp9.1_initial_prob.py --graph_name Facebook
# python plot/plot9.1_initial_prob.py

python optimization/exp9.2_rec_prob.py --graph_name Facebook
python plot/plot9.2_rec_prob.py

# python optimization/exp9.3_adopt_prob.py --graph_name Facebook
# python plot/plot9.3_adopt_prob.py

## part 3: run the optimization in Section 7 (For Yelp graph)
# python optimization/exp9.1_initial_prob.py --graph_name Yelp
# python plot/plot_Yelp9.1_initial_prob.py

# python optimization/exp9.2_rec_prob.py --graph_name Yelp
# python plot/plot_Yelp9.2_rec_prob.py

# python optimization/exp9.3_adopt_prob.py --graph_name Yelp
# python plot/plot_Yelp9.3_adopt_prob.py

## part 4: run the posterior sampling reinforcement learning algorithms on Facebook's graph
# python optimization/exp9.1_initial_prob.py --graph_name Facebook --enable_PSRL
# python plot/plot_TS9.1_initial_prob.py

# python optimization/exp9.2_rec_prob.py --graph_name Facebook --enable_PSRL
# python plot/plot_TS9.2_rec_prob.py

# python optimization/exp9.3_adopt_prob.py --graph_name Facebook --enable_PSRL
# python plot/plot_TS9.3_adopt_prob.py

### part 5: compare a firm's profit for different $k$
python optimization/exp9.7_compare_influence.py
python plot/plot_9.7_compare_influence_k.py

### part 6: compare the running time between agent-based simulation and our algorithm
# to run this, please download user.json (Yelp) from https://1drv.ms/u/s!AuhX-fJM-sJvgnIzJhDUsQiCczhN?e=OsTVbK, and put it under the folder/data
# python simulation/exp10_compare_time.py

