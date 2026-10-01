<?php
/**
 * TLS — Transformative Leadership Systems: brand-specific setup.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

add_filter( 'tls_google_fonts_url', function () {
    return 'https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Lato:wght@400;700&family=Playfair+Display:ital@1&display=swap';
} );
