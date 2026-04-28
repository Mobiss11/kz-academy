# Instagram Looter — verified response shapes

> ✅ **Источник:** все 30 эндпоинтов прозвонены реальными API-вызовами на Basic-плане 2026-04-28. Длинные подписанные CDN-URL замаскированы как `<url>`. Числовые ID профилей и постов — реальные публичные.
>
> Этот файл — **canonical reference** для проверки имён полей. Если ученик пишет код и сомневается в названии поля — grep по этому файлу.

## /id — username ↔ user_id

```jsonc
// GET /id?username=zuck → 200
// GET /id?id=314216 → 200
{
  "status": true,
  "username": "zuck",
  "user_id": "314216",
  "attempts": "3"          // внутренний счётчик ретраев провайдера
}
```

## /id-media — URL ↔ media_id

```jsonc
// GET /id-media?id=<media_id> → 200
// GET /id-media?url=<post_url> → 200
{
  "status": true,
  "shortcode": "DWuq1e1D1E6",
  "media_id": "<numeric_id>"
}
```

## /profile — публичный профиль (web-API формат)

```jsonc
// GET /profile?username=zuck (или ?id=314216) → 200
// Top-level keys (62), nested fields shown
{
  "status": true,
  "ai_agent_owner_username": null,
  "biography": "...",
  "bio_links": [],
  "fb_profile_biolink": null,
  "biography_with_entities": { "raw_text": "...", "entities": [] },
  "blocked_by_viewer": false,
  "restricted_by_viewer": null,
  "country_block": false,
  "eimu_id": "<id>",
  "external_url": null,
  "external_url_linkshimmed": null,
  "edge_followed_by": { "count": 14000000 },
  "fbid": "<id>",
  "followed_by_viewer": false,
  "edge_follow": { "count": 600 },
  "follows_viewer": false,
  "full_name": "...",
  "group_metadata": null,
  "has_ar_effects": false,
  "has_clips": true,
  "has_guides": false,
  "has_channel": false,
  "has_blocked_viewer": false,
  "highlight_reel_count": 35,
  "has_onboarded_to_text_post_app": true,
  "has_requested_viewer": false,
  "hide_like_and_view_counts": false,
  "id": "314216",
  "is_business_account": false,
  "is_professional_account": true,
  "is_supervision_enabled": false,
  "is_guardian_of_viewer": false,
  "is_supervised_by_viewer": false,
  "is_supervised_user": false,
  "is_embeds_disabled": false,
  "is_joined_recently": false,
  "guardian_id": null,
  "business_address_json": null,
  "business_contact_method": "UNKNOWN",
  "business_email": null,
  "business_phone_number": null,
  "business_category_name": null,
  "overall_category_name": null,
  "category_enum": null,
  "category_name": "Personal Blog",
  "is_private": false,
  "is_verified": true,
  "is_verified_by_mv4b": false,
  "is_regulated_c18": false,
  "pinned_channels_list_count": 0,
  "profile_pic_url": "<url>",
  "profile_pic_url_hd": "<url>",
  "requested_by_viewer": false,
  "should_show_category": true,
  "should_show_public_contacts": false,
  "show_account_transparency_details": true,
  "show_text_post_app_badge": null,
  "remove_message_entrypoint": false,
  "transparency_label": null,
  "transparency_product": null,
  "username": "zuck",
  "edge_owner_to_timeline_media": { "count": 312, "edges": [/* posts */] }
}
```

## /profile2 — internal IG mobile API формат

```jsonc
// GET /profile2?username=zuck (или ?id=314216) → 200
// Top-level keys (60)
{
  "status": true, "fbid_v2": "<id>",
  "is_memorialized": false, "is_private": false,
  "has_story_archive": null, "is_coppa_enforced": null,
  "supervision_info": null, "is_regulated_c18": false,
  "regulated_news_in_locations": null,
  "bio_links": [], "linked_fb_info": null,
  "text_post_app_badge_label": null, "show_text_post_app_badge": null,
  "username": "zuck", "pk": "314216",
  "live_broadcast_visibility": 0, "live_broadcast_id": null,
  "profile_pic_url": "<url>",
  "hd_profile_pic_url_info": { "url": "<url>", "width": 1080, "height": 1080 },
  "is_unpublished": false, "latest_reel_media": 0, "has_profile_pic": true,
  "profile_pic_genai_tool_info": [],
  "biography": "...", "full_name": "...",
  "is_verified": true, "show_account_transparency_details": true,
  "account_type": 3,
  "follower_count": 14000000, "mutual_followers_count": 0,
  "profile_context_links_with_user_ids": [],
  "profile_context_facepile_users": [],
  "address_street": "", "city_name": "",
  "is_business": false, "zip": "",
  "biography_with_entities": { "entities": [] },
  "category": "Personal Blog", "should_show_category": true,
  "is_ring_creator": false, "show_ring_award": false,
  "ring_creator_metadata": null, "account_badges": [],
  "external_lynx_url": null, "external_url": null,
  "transparency_label": null, "transparency_product": null,
  "hide_creator_marketplace_badge": false,
  "id": "314216",
  "has_chaining": true, "remove_message_entrypoint": false,
  "is_embeds_disabled": false, "is_cannes": false,
  "is_professional_account": true, "following_count": 600,
  "media_count": 312, "total_clips_count": 50,
  "has_visible_media_notes": false,
  "latest_besties_reel_media": 0, "reel_media_seen_timestamp": 0,
  "attempts": "1"
}
```

## /web-profile — raw GraphQL response

```jsonc
// GET /web-profile?username=zuck → 200
// Это сырой GraphQL-ответ Instagram. Поля идентичны /profile, обёрнутые в data.user.
{
  "data": {
    "user": {
      "ai_agent_owner_username": null,
      "ai_agent_type": null,
      "biography": "...",
      "bio_links": [],
      "fb_profile_biolink": null,
      "biography_with_entities": { "raw_text": "...", "entities": [] },
      "blocked_by_viewer": false,
      "restricted_by_viewer": null,
      "country_block": false,
      "eimu_id": "<id>",
      // ...тот же набор полей что у /profile, без обёртки status
    }
  }
}
```

## /user-feeds — лента постов V1 (max_id-пагинация)

```jsonc
// GET /user-feeds?id=314216&count=30 → 200
{
  "more_available": true,
  "items": [
    {
      "strong_id__": "<id>", "id": "<post_id>",
      "caption_is_edited": false, "device_timestamp": 0,
      "filter_type": 0, "like_and_view_counts_disabled": false,
      "fbid": "<id>", "deleted_reason": 0,
      "client_cache_key": "<x>", "integrity_review_decision": null,
      "pk": "<post_pk>",
      "has_delayed_metadata": false, "mezql_token": "",
      "should_request_ads": false,
      "has_privately_liked": false, "is_quiet_post": false,
      "profile_grid_thumbnail_fitting_style": "...",
      "collaborator_edit_eligibility": null,
      "share_count_disabled": false, "has_shared_to_fb": 0,
      "subtype_name_for_REST__": "...",
      "has_views_fetching_on_search_grid": false,
      "code": "<shortcode>",
      "enable_media_notes_production": false,
      "has_views_fetching": false,
      "original_media_has_visual_reply_media": false,
      "image_versions2": { "candidates": [{ "url": "<url>", "width": 1080, "height": 1080 }] },
      // ...плюс caption, media_type, like_count, comment_count, play_count, taken_at, user, ...
    },
    /* +29 more items */
  ]
}
```

## /user-feeds2 — лента постов V2 (end_cursor пагинация)

```jsonc
// GET /user-feeds2?id=314216&count=30 → 200
{
  "data": {
    "user": {
      "edge_owner_to_timeline_media": {
        "count": 312,
        "page_info": { "has_next_page": true, "end_cursor": "<cursor>" },
        "edges": [
          {
            "node": {
              "__typename": "GraphSidecar",  // или GraphImage / GraphVideo
              "id": "<media_id>",
              "gating_info": null,
              "fact_check_overall_rating": null, "fact_check_information": null,
              "media_overlay_info": null,
              "sensitivity_friction_info": null,
              "sharing_friction_info": { "should_have_sharing_friction": false, "bloks_app_url": null },
              "dimensions": { "height": 1350, "width": 1080 },
              "display_url": "<url>",
              "display_resources": [
                { "src": "<url>", "config_width": 640, "config_height": 800 }
                /* +N more */
              ],
              "shortcode": "<shortcode>",
              "edge_media_to_caption": { "edges": [{ "node": { "text": "..." } }] },
              "edge_media_to_comment": { "count": 123 },
              "comments_disabled": false,
              "taken_at_timestamp": 1700000000,
              "edge_liked_by": { "count": 1234 },
              "edge_media_preview_like": { "count": 1234 },
              "owner": { "id": "...", "username": "..." },
              "thumbnail_src": "<url>"
            }
          }
        ]
      }
    }
  }
}
```

## /reels — рилсы (max_id пагинация)

```jsonc
// GET /reels?id=314216&count=30 → 200
{
  "items": [
    {
      "media": {
        "strong_id__": "<id>", "id": "<media_id>",
        "disable_caption_and_comment": false, "fbid": "<id>",
        "deleted_reason": 0, "client_cache_key": "<x>",
        "integrity_review_decision": null, "pk": "<pk>",
        "is_affiliate_commission_eligible": false,
        "has_delayed_metadata": false, "mezql_token": "",
        "should_request_ads": false, "has_privately_liked": false,
        "is_quiet_post": false,
        "collaborator_edit_eligibility": null,
        "share_count_disabled": false,
        "is_reshare_of_text_post_app_media_in_ig": null,
        "translated_langs_for_autodub": null,
        "subtype_name_for_REST__": "...",
        "is_third_party_downloads_eligible": false,
        "image_versions2": {
          "additional_candidates": { "first_frame": { "url": "<url>", "width": 1080, "height": 1920 } },
          "candidates": [...]
        },
        // ...плюс video_versions, music_metadata, caption, taken_at, like_count, comment_count, play_count
      }
    }
  ]
}
```

## /user-reposts — репосты пользователя

```jsonc
// GET /user-reposts?id=314216 → 200
{
  "more_available": true,
  "items": [
    {
      "id": "<repost_id>",
      "all_previous_submitters": [],
      "carousel_media": [
        {
          "__typename": "...",
          "strong_id__": "<id>", "id": "<id>", "carousel_parent_id": "<id>",
          "image_versions2": { "candidates": [...] },
          "smart_thumbnail_enabled": false,
          "media_type": 1,  // 1=photo, 2=video, 8=carousel
          "original_height": 1080, "original_width": 1080,
          "pk": "<pk>",
          "commerciality_status": "...",
          "explore_hide_comments": false,
          "has_audio": false, "has_liked": false
        }
      ]
    }
  ]
}
```

## /user-tags — посты, где отметили юзера (end_cursor)

```jsonc
// GET /user-tags?id=314216&count=30 → 200
{
  "data": {
    "user": {
      "edge_user_to_photos_of_you": {
        "count": 1234,
        "page_info": { "has_next_page": true, "end_cursor": "<cursor>" },
        "edges": [
          {
            "node": {
              "id": "...", "__typename": "GraphImage",
              "edge_media_to_caption": { "edges": [{ "node": { "text": "..." } }] },
              "shortcode": "...",
              "edge_media_to_comment": { "count": 1 },
              "comments_disabled": false,
              "taken_at_timestamp": 1700000000,
              "dimensions": { "height": 1080, "width": 1080 },
              "display_url": "<url>",
              "edge_liked_by": { "count": 12 },
              "edge_media_preview_like": { "count": 12 },
              "owner": { "id": "...", "username": "..." },
              "thumbnail_src": "<url>"
            }
          }
        ]
      }
    }
  }
}
```

## /related-profiles — похожие аккаунты

```jsonc
// GET /related-profiles?id=314216 → 200
{
  "data": { "viewer": { "user": { "edge_related_profiles": { "edges": [/* nodes */] } } } },
  "status": true,
  "attempts": "1"
}
```

## /post — детали поста

```jsonc
// GET /post?url=<post_url>  ИЛИ  ?id=<media_id> → 200
{
  "status": true,
  "__typename": "GraphSidecar",   // или GraphImage / GraphVideo
  "id": "<media_id>",
  "shortcode": "DWuq1e1D1E6",
  "thumbnail_src": "<url>",
  "dimensions": { "height": 1350, "width": 1080 },
  "gating_info": null,
  "fact_check_overall_rating": null,
  "fact_check_information": null,
  "sensitivity_friction_info": null,
  "sharing_friction_info": { "should_have_sharing_friction": false, "bloks_app_url": null },
  "media_overlay_info": null,
  "media_preview": "...",  // base64 mini-preview
  "display_url": "<url>",
  "display_resources": [
    { "src": "<url>", "config_width": 640, "config_height": 800 },
    { "src": "<url>", "config_width": 750, "config_height": 937 },
    { "src": "<url>", "config_width": 1080, "config_height": 1350 }
  ],
  "is_video": false,
  "tracking_token": "<x>",
  "upcoming_event": null,
  "edge_media_to_tagged_user": { "edges": [] },
  "owner": { "id": "...", "username": "...", "is_verified": true, /* + ~30 owner fields */ },
  "accessibility_caption": null,
  "edge_sidecar_to_children": { "edges": [/* для каруселей */] }
}
```

## /post-dl — прямые ссылки на медиа

```jsonc
// GET /post-dl?url=<post_url> → 200
{
  "data": {
    "full_name": "...", "username": "...",
    "medias": [
      { "type": "video", "link": "<url>", "img": "<url>" },
      { "type": "image", "link": "<url>" }
    ],
    "comment_count": 123,
    "like_count": 4567,
    "taken_at_timestamp": 1700000000,
    "caption": "..."
  },
  "status": true,
  "attempts": "1"
}
```

## /music — посты с конкретным треком

```jsonc
// GET /music?id=<music_id>&max_id=... → 200
// Если нет данных или произошёл сбой ретрая:
{ "attempts": "10022" }
// Если есть данные — структура аналогична /user-feeds (items[])
```

## /tag-feeds — посты по хэштегу

```jsonc
// GET /tag-feeds?query=travel → 200
{
  "data": {
    "hashtag": {
      "id": "...", "name": "travel",
      "allow_following": true, "is_following": false,
      "is_top_media_only": false,
      "profile_pic_url": "<url>",
      "edge_hashtag_to_media": {
        "count": 12345,
        "page_info": { "has_next_page": true, "end_cursor": "<cursor>" },
        "edges": [
          {
            "node": {
              "comments_disabled": false,
              "__typename": "GraphImage",
              "id": "...",
              "edge_media_to_caption": { "edges": [{ "node": { "text": "..." } }] },
              "shortcode": "...",
              "edge_media_to_comment": { "count": 12 },
              "taken_at_timestamp": 1700000000,
              "dimensions": { "height": 1080, "width": 1080 },
              "display_url": "<url>"
            }
          }
        ]
      }
    }
  }
}
```

## /location-info — инфа о локации

```jsonc
// GET /location-info?id=212988663 → 200
{
  "location_info": {
    "name": "New York, New York",
    "phone": "",
    "category": "Government organization",
    "media_count": 82334189,
    "price_range": 3,
    "lat": 40.7142, "lng": -74.0064,
    "slug": "new-york-new-york",
    "location_id": "212988663",
    "location_address": "", "location_city": "", "location_zip": "",
    "ig_business": { "profile": "null" },
    "hours": { "status": "" }
  },
  "attempts": "10"
}
```

## /location-feeds — посты в локации

```jsonc
// GET /location-feeds?id=212988663&tab=top → 200
{
  "edges": [
    {
      "node": {
        "code": "<shortcode>", "pk": "<pk>", "id": "<id>_<owner_id>",
        "ad_id": null, "boosted_status": null,
        "boost_unavailable_identifier": null, "boost_unavailable_reason": null,
        "caption": {
          "has_translation": false, "created_at": 1700000000,
          "pk": "<caption_pk>",
          "text": "...", "caption_is_edited": false
        },
        "feed_demotion_control": null,
        "feed_recs_demotion_control": null,
        "taken_at": 1700000000,
        "inventory_source": "...",
        "video_versions": [...],
        "is_dash_eligible": 0,
        "number_of_qualities": 1,
        "video_dash_manifest": "<xml_string>",
        "image_versions2": { "candidates": [{ "url": "<url>", "height": 1080, "width": 1080 }] }
      }
    }
  ]
}
```

## /cities — города по стране

```jsonc
// GET /cities?country_code=US → 200
{
  "country_info": { "id": "US", "name": "United States", "slug": "united-states" },
  "city_list": [
    { "id": "c2753900", "name": "Downtown-PennQuarter-Chinatown", "slug": "..." },
    { "id": "c2728343", "name": "CivicCenter", "slug": "..." }
    /* +N more */
  ]
}
```

## /locations — локации в городе

```jsonc
// GET /locations?city_id=c2753900 → 200
{
  "country_info": { "id": "US", "name": "...", "slug": "..." },
  "city_info": { "id": "c2753900", "name": "...", "slug": "..." },
  "location_list": [
    { "id": "372247132", "name": "...", "slug": "..." }
    /* +N more */
  ]
}
```

## /sections — список Explore-категорий

```jsonc
// GET /sections → 200
{
  "sections": [
    {
      "section_id": "...",
      "name": "...",
      "subsections": [
        {
          "section_id": "...",
          "name": "...",
          "medias": [ /* IG Media-объекты, как в /user-feeds */ ]
        }
      ]
    }
  ]
}
```

## /section — медиа в Explore-категории

```jsonc
// GET /section?id=<section_id>&count=30 → 200
{
  "section_name": "...",
  "max_id": "<cursor>",
  "more_available": true,
  "items": [/* IG Media-объекты, как в /user-feeds */]
}
```

## /search — 4 формы (users / hashtags / locations / global)

```jsonc
// GET /search?query=tesla&select=users → 200
{
  "status": true,
  "users": [
    {
      "position": 0,
      "user": {
        "username": "tesla", "is_verified": true, "full_name": "Tesla",
        "search_social_context": "...", "unseen_count": 0,
        "pk": "<pk>",
        "live_broadcast_visibility": 0, "live_broadcast_id": null,
        "latest_reel_media": 0, "seen": 0,
        "profile_pic_url": "<url>",
        "is_unpublished": false,
        "id": "<id>"
      }
    }
  ]
}

// GET /search?query=tesla&select=hashtags → 200
{
  "status": true,
  "hashtags": [
    { "position": 0, "hashtag": { "name": "tesla", "media_count": 12345, "id": "<id>" } }
  ]
}

// GET /search?query=berlin&select=locations → 200
{
  "status": true,
  "places": [
    {
      "position": 0,
      "place": {
        "location": { "pk": "<pk>", "name": "...", "facebook_places_id": "<id>" },
        "subtitle": "...",
        "title": "..."
      }
    }
  ]
}

// GET /search?query=tesla → 200 (global)
{
  "status": true,
  "hashtags": [...],
  "places": [...],
  "users": [...]
}
```
