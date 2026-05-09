package com.lms.app.ui.notifications

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.LinearLayoutManager
import com.lms.app.databinding.FragmentNotificationsBinding
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class NotificationsFragment : Fragment() {

    private var _binding: FragmentNotificationsBinding? = null
    private val binding get() = _binding!!
    private val viewModel: NotificationViewModel by viewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentNotificationsBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.rvNotifications.layoutManager = LinearLayoutManager(requireContext())

        // Bildirişlər siyahısını müşahidə et
        viewModel.notifications.observe(viewLifecycleOwner) { list ->
            if (list.isEmpty()) {
                binding.layoutEmpty.visibility = View.VISIBLE
                binding.rvNotifications.visibility = View.GONE
            } else {
                binding.layoutEmpty.visibility = View.GONE
                binding.rvNotifications.visibility = View.VISIBLE
                // TODO: NotificationAdapter — Phase 2
            }
        }

        // Oxunmamış sayını başlıqda göstər
        viewModel.unreadCount.observe(viewLifecycleOwner) { count ->
            activity?.title = if (count > 0) "Bildirişlər ($count)" else "Bildirişlər"
        }

        // Bildirişləri yüklə
        viewModel.loadNotifications()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
