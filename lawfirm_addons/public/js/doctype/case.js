frappe.ui.form.on('Case', {
	refresh: function(frm) {
		frm.add_custom_button(__('View Attachments'), function() {
			const url = `/document-reader?case=${encodeURIComponent(frm.doc.name)}`;
			window.open(url, '_blank');
		}, __('Actions'));

		// Override attachment link clicks to redirect to document-reader
		function setupAttachmentRedirects() {
			if (!frm.attachments || !frm.attachments.parent) return;
			
			// Find all attachment file links (not the lock icon)
			frm.attachments.parent.find('.data-pill a[href*="/files/"]').each(function() {
				const $link = $(this);
				const href = $link.attr('href');
				
				// Skip lock icon links and already handled links
				if (href && href.includes('/app/file/')) return;
				if ($link.hasClass('case-redirect-handled')) return;
				
				$link.addClass('case-redirect-handled');
				$link.off('click.case-redirect').on('click.case-redirect', function(e) {
					e.preventDefault();
					e.stopPropagation();
					const case_url = `/document-reader?case=${encodeURIComponent(frm.doc.name)}`;
					window.open(case_url, '_blank');
					return false;
				});
			});
		}

		// Setup redirects immediately and after a delay (for dynamic attachments)
		setupAttachmentRedirects();
		setTimeout(setupAttachmentRedirects, 300);
		
		// Also setup when attachments are refreshed
		if (frm.attachments && typeof frm.attachments.refresh === 'function') {
			const originalRefresh = frm.attachments.refresh;
			frm.attachments.refresh = function() {
				originalRefresh.apply(this, arguments);
				setTimeout(setupAttachmentRedirects, 100);
			};
		}
	}
});