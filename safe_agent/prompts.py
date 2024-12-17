# flake8: noqa


RISK_QUANTIFICATION = """
According to the structure of the risk field formulation, if the quantified perceived risk from a surrounding vehicle is high, there are several potential reasons. Keep the followings in mind when the QPR is elevated:
1. The distance between the ego vehicle and the surrounding vehicle is short. Vehicles might be too close to each other.
2. The speed of either the ego vehicle or the surrounding vehicle is high, which usually happens when one vehicle is overtaking the other.
3. The heading angle of the ego vehicle or the surrounding vehicle is towards the other, which usually happens during lane changes or cutting in."""


SYSTEM_MESSAGE = """
You are ChatGPT, a large language model trained by OpenAI. Now you act as a mature driving assistant, who can give accurate and correct advice for human driver in complex urban driving scenarios.
You will be given a detailed description of the driving scenario of current frame along with your history of previous decisions. You will also be given the available actions you are allowed to take. There is no rush to give a final answer unless you are confident that the answer is correct.

Your response should use the following format:
<reasoning>
<reasoning>
<repeat until you have a decision>
Response to user:<only output one `Action_id` as a int number of you decision, without any action name or explanation. The output decision must be unique and not ambiguous, for example if you decide to decelearate, then output `4`> 

Make sure to include {delimiter} to separate every step.
"""

example_message = textwrap.dedent(f"""\
        {delimiter} Driving scenario description:
        You are driving on a highway road with 2 lanes, and you are currently driving in the left lane. Navigation instructions suggest a lane change to the right lane. 
        Your current position is (381.69, 22.82), speed is (34.51, 0.14) m/s, acceleration is (0.15, 0.09) m/s^2, total quantified perceived risk is 67993.57. There are other vehicles driving around you, and below is their basic information:
        - Vehicle `6.0` is driving in front in the right lane. Position: (401.21, 26.58), Speed: (23.38, 0.07) m/s, Acceleration: (0.02, 0.03) m/s^2, quantified perceived risk: 55962.14. 
        - Vehicle `10.0` is driving behind you in the right lane . Position: (358.45, 26.72), Speed: (22.31, 0.14) m/s, Acceleration: (-0.13, -0.01) m/s^2, quantified perceived risk: 6341.43
        - Vehicle `11.0` is driving behind you in the left lane. Position: (347.83, 24.55), Speed: (24.97, -1.16) m/s, Acceleration: (0.78, 0.04) m/s^2, quantified perceived risk: 5689.99
          Vehicles 10, 11 exhibit minimal risk levels, requiring no immediate intervention.
          Vehicle 6 exhibits exceptional risk. Exercise rigorous caution with these vehicles, and avoid taking actions involving them until the risk is sufficiently mitigated.

        Risk Quantification Structure: 
        According to the structure of the risk field formulation, if the quantified perceived risk from a surrounding vehicle is high, there are several potential reasons. Keep the followings in mind when the QPR is elevated:
        1. The distance between the ego vehicle and the surrounding vehicle is short. Vehicles might be too close to each other.
        2. The speed of either the ego vehicle or the surrounding vehicle is high, which usually happens when one vehicle is overtaking the other.
        3. The heading angle of the ego vehicle or the surrounding vehicle is towards the other, which usually happens during lane changes or cutting in.

        When making a decision, you should consider all vehicles that will be involved by the decision in the surroundings, from different aspects, including time headway, time to collision, responsibility-sensitive safety, and the quantified risk.
        You can use all your knowledge to make decisions. The few shot answers template passed by AI message is just an example of reasoning steps. Feel free to come up with better structures that help choose a reasonable action.


        {delimiter} Your available actions:
        IDLE - remain in the current lane with current speed, Action_id: 0
        Turn-left - change lane to the left of the current lane, Action_id: 1
        Turn-right - change lane to the right of the current lane, Action_id: 2
        Acceleration - accelerate the vehicle, Action_id: 3
        Deceleration - decelerate the vehicle, Action_id: 4
        """)
example_answer = textwrap.dedent(f"""\
        Well, I have 5 actions to choose from. Now, I would like to know which action is possible. 
        If navigation shows changing lane, I need to first check if I can change lane, then idle, then decelerate.
        If navigation shows I can keep my current lane, I should first check if I can accelerate, then idle, finally decelerate. 

        - I want to know if I can change lane to the right, so I need to observe the car in the right lane, which is car `6`. The distance between me and car `6` is 401.21 - 381.69 = 19.52 m, and the difference in speed is 34.51 - 23.38 = 11.13 m/s. Car `912` is traveling 19.52 m ahead of me and its speed is 11.13 m/s slower than mine. This distance is too close and my speed is too high, so I should not change lane to the right now.
        - Since I cannot change lane, I want to know if I can maintain my current speed. I need to observe the car in front of me on the current lane, or any cars that are cutting in. There are no such cars in this frame.
        - It is ok for me to keep my current speed, and wait for another opportunity to change lane to the right later.
        - Now my option is to idle.
        Final Answer: IDLE
                                         
        Response to user:#### 0
        """)


