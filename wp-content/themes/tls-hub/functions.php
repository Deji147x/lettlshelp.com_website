<?php
/**
 * TLS — LetTLSHelp (hub): brand-specific setup.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

add_filter( 'tls_google_fonts_url', function () {
    return 'https://fonts.googleapis.com/css2?family=Lora:wght@500;600&family=Open+Sans:wght@400;600;700&family=Playfair+Display:ital@1&display=swap';
} );
