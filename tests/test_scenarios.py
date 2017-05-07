test_scenarios_parser = [
    (
        '<rss><channel> <item>'
        '   <title>Title</title>'
        '   <link>URL Link</link>'
        '   <description>'
        '       <p>P Content</p>'
        '   </description>'
        '</item> </channel></rss>',
        {
            'feed': [
                 {
                    'title': 'Title',
                    'link': 'URL Link',
                    'description': [
                        {
                            'type': 'text',
                            'content': 'P Content'
                        },
                    ]
                 },
            ]
        }
    ),
    (
        '<rss><channel> <item>'
        '   <title>Title</title>'
        '   <link>URL Link</link>'
        '   <description>'
        '       <div><img src=\'www.google.com\'/></div>'
        '   </description>'
        '</item> </channel></rss>',
        {
            'feed': [
                 {
                    'title': 'Title',
                    'link': 'URL Link',
                    'description': [
                        {
                            'type': 'image',
                            'content': 'www.google.com'
                        },
                    ]
                 },
            ]
        }
    ),
    (
        '<rss><channel> <item>'
        '   <title>Title</title>'
        '   <link>URL Link</link>'
        '   <description>'
        '       <div><ul>'
        '           <li>Content LI1</li>'
        '           <li>Content LI2</li>'
        '           <li>Content LI3</li>'
        '       </ul></div>'
        '   </description>'
        '</item> </channel></rss>',
        {
            'feed': [
                 {
                    'title': 'Title',
                    'link': 'URL Link',
                    'description': [
                        {
                            'type': 'links',
                            'content': ['Content LI1', 'Content LI2', 'Content LI3']
                        }
                    ]
                 },
            ]
        }
    ),
    (
        '<rss><channel> <item>'
        '   <title>Title</title>'
        '   <link>URL Link</link>'
        '   <description>'
        '       <div><ul>'
        '           <li>Content LI1</li>'
        '           <li>Content LI2</li>'
        '           <li>Content LI3</li>'
        '       </ul></div>'
        '       <p>P Content</p>'
        '       <div><img src=\'www.google.com\'/></div>'
        '   </description>'
        '</item> </channel></rss>',
        {
            'feed': [
                 {
                    'title': 'Title',
                    'link': 'URL Link',
                    'description': [
                        {
                            'content': 'P Content',
                            'type': 'text',
                        },
                        {
                            'content': ['Content LI1', 'Content LI2', 'Content LI3'],
                            'type': 'links',
                        },
                        {
                            'content': 'www.google.com',
                            'type': 'image',

                        },
                    ]
                 },
            ]
        }
    ),
]

test_scenarios_items_elements = [
    ('<rss><channel></channel></rss>', 0),
    ('<rss><channel> <item></item> <item></item> </channel></rss>', 2)
]
