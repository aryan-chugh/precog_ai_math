## Why I could complete my work on time...
#### Although I know that none of the reasons I give now should be considered valid in justifying my inabaility to complete the task (rather they'd be plain excuses).
I was involved in the quizzes for the earlier part and then soon after the quizzes ended much of my time got consumed playing in an intercollege cricket tournament. I regret the fact that I couldn't put my complete efforts into the project.

Probably, with more of my efforts I could have pulled off a better presentable and accurate report.

## Measures which can be used to check how well the model has been trained:
#### Coarse metrics: 
--- Accuracy: %-correctness could serve as a very rough metric, providing no information about  the type of patterns the AI model learns. Expected comparison method employed using this metric would involve a simple comparison of the accuracy measures of the zero-shot, few-shot and CoT style of prompting.

I tried to use this imetric (purely due to time constraints).. My work was not completed to reach a satisfaction level, but the expected behavior of this metric considering well-formed few-shot and CoT prompts should be:
                Zero-Shot < Few-Shot < Chain of Thought

#### Very detailed metrics:
--- We need to trace the test samples to the input samples and classify, manually the extent of similarity (which again is an abstractly defined concept => may use it to be a similar transition-set structure and and similar application orders in the correct solution.)... 

Now, this would yield the following categories for each of the test-set sample:
    1. Very similar to the train-set examples => ability of the model to learn well-defined concepts. 
    2. Somewhat similar to the train-set examples => slight extension of the logic to lesser-known problems.
    3. Very dissimilar (no direct correspondences exist in the training set) => pure creativity exhibited by the model.

Now for the categories 1, 2 there is an expected increase in the accuracy from Zero shot to the Chain of Thought approaches, while for the 3rd category, the performance of all the prompting methods is expected to be more-or-less similar.

## Why is the accuracy of the responses low even in the CoT prompting?
    Reason 1: probably need more examples, somewhat more elaborate, than the existing ones, in the explanation; for the LLM model to understand the thinking behind the solution.
    
    Reason 2: Somewhat more similarity in the samples from the system-provided dataset and tested dataset would surely help in improvidng efficiency. [currently, if we think of them as distributions, then the distributions could be treated as very different].
    
## Where does the AI lag from the humans.
Addition of problem specific hints into the sets of transitions, which otherwise aid the humans to solve the question by narrowing the search space, but the AI still has to solve it from scratch. [This metric needs to be considered when comparing human and LLM performance!]

Real world visualisation (ex. the bow problem) linking which the humans could make on reading the problem, but the AI can't.

## Could something be done about it?
More training of the LLM on such examples, teaching it how to use up the inside-problem hints.. probably could make some difference although, still I wouldn't expect a marked change from the original model, since there is still a creativity factor involved that separates the human mind from the AI.

Secondly, name of the problem could be indicated to the AI model via the transitions set. The visualisation part, where the AI needs to reason out based on some given pattern in the real world counterpart of the problem, will still take a lot of research to figure out.

## Where does the human mind stay behind?
Since I was the curator of the problems (representative of the human mind) and preferrably put the problems which I had solved correctly into the dataset, there is not much (specifically zero) data to remark on this question.

The expected behaviour could be:
    As we know humans could simultaneously think of 7-9 things/ideas. Whereas there is no such defined limit on the LLM computation. Hence, in the examples wherein the required sequence of transitions to be thought of is large, AI could be better in providing the solution provided it is given enough time to reason without cutting off earlier.

    [purely computational tasks which need to keep a larger set of transitions, could favour AI responses over the humans]. 