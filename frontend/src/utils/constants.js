export const AVAILABLE_MODELS = [
    {
        provider: 'OpenAI',
        models: [
            { id: 'gpt-4o', name: 'GPT-4o', description: 'Most capable OpenAI model' },
            { id: 'gpt-4o-mini', name: 'GPT-4o Mini', description: 'Fast & affordable' },
            { id: 'gpt-4-turbo', name: 'GPT-4 Turbo', description: 'High intelligence model' },
            { id: 'o1-mini', name: 'o1-mini', description: 'Reasoning model' },
        ],
    },
    {
        provider: 'Anthropic',
        models: [
            { id: 'claude-3.5-sonnet', name: 'Claude 3.5 Sonnet', description: 'Most intelligent Claude' },
            { id: 'claude-3.5-haiku', name: 'Claude 3.5 Haiku', description: 'Fastest Claude model' },
            { id: 'claude-3-opus', name: 'Claude 3 Opus', description: 'Powerful & thorough' },
        ],
    },
    {
        provider: 'Google',
        models: [
            { id: 'gemini-2.0-flash', name: 'Gemini 2.0 Flash', description: 'Latest Gemini model' },
            { id: 'gemini-1.5-pro', name: 'Gemini 1.5 Pro', description: 'Long context model' },
            { id: 'gemini-1.5-flash', name: 'Gemini 1.5 Flash', description: 'Fast & efficient' },
        ],
    },
    {
        provider: 'Open Source',
        models: [
            { id: 'llama-3.1-70b', name: 'Llama 3.1 70B', description: 'Meta\'s flagship open model' },
            { id: 'mixtral-8x7b', name: 'Mixtral 8x7B', description: 'Mistral MoE model' },
            { id: 'deepseek-v3', name: 'DeepSeek V3', description: 'Advanced reasoning' },
        ],
    },
];

export const MOCK_NOTES = {
    title: 'Attention Is All You Need',
    authors: 'Vaswani et al., 2017',
    sections: [
        {
            heading: 'Abstract',
            content:
                'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.',
        },
        {
            heading: 'Introduction',
            content:
                'Recurrent neural networks, long short-term memory and gated recurrent neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems. The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality.',
        },
        {
            heading: 'Model Architecture',
            content:
                'The Transformer follows an encoder-decoder structure using stacked self-attention and point-wise, fully connected layers for both the encoder and decoder. The encoder maps an input sequence of symbol representations to a sequence of continuous representations. The decoder then generates an output sequence of symbols one element at a time.',
        },
        {
            heading: 'Multi-Head Attention',
            content:
                'Instead of performing a single attention function with d_model-dimensional keys, values and queries, it is beneficial to linearly project the queries, keys and values h times with different, learned linear projections. Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions.',
        },
        {
            heading: 'Results',
            content:
                'On the WMT 2014 English-to-German translation task, the big transformer model outperforms the best previously reported models including ensembles by more than 2.0 BLEU, establishing a new state-of-the-art BLEU score of 28.4. On the WMT 2014 English-to-French translation task, our model achieves a new single-model state-of-the-art BLEU score of 41.0.',
        },
        {
            heading: 'Conclusion',
            content:
                'The Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequence-aligned RNNs or convolution. The Transformer can be trained significantly faster than architectures based on recurrent or convolutional layers and achieves new state of the art results.',
        },
    ],
};

export const MOCK_CHAT_MESSAGES = [
    {
        role: 'assistant',
        content: 'Hello! I\'ve analyzed the research paper. Feel free to ask me any questions about its content, methodology, results, or implications.',
    },
];

export const APP_NAME = 'ResearchLens';

export const NAV_LINKS = [
    { label: 'Features', href: '/#features' },
    { label: 'How It Works', href: '/#how-it-works' },
    { label: 'About', href: '/#about' },
];
