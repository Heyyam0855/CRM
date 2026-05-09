package com.lms.app.ui.bookings

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.lms.app.R
import com.lms.app.databinding.FragmentBookingListBinding
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class BookingListFragment : Fragment() {

    private var _binding: FragmentBookingListBinding? = null
    private val binding get() = _binding!!
    private val viewModel: BookingViewModel by viewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentBookingListBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.rvBookings.layoutManager = LinearLayoutManager(requireContext())

        // Yeni dərs düyməsi → Booking Calendar-a keç
        binding.btnBookNow.setOnClickListener {
            findNavController().navigate(R.id.action_bookings_to_calendar)
        }

        // Dərs siyahısını müşahidə et
        viewModel.bookings.observe(viewLifecycleOwner) { list ->
            if (list.isEmpty()) {
                binding.layoutEmpty.visibility = View.VISIBLE
                binding.rvBookings.visibility = View.GONE
            } else {
                binding.layoutEmpty.visibility = View.GONE
                binding.rvBookings.visibility = View.VISIBLE
                // TODO: BookingAdapter — Phase 2
            }
        }

        viewModel.isLoading.observe(viewLifecycleOwner) { loading ->
            binding.btnBookNow.isEnabled = !loading
        }

        viewModel.error.observe(viewLifecycleOwner) { msg ->
            if (!msg.isNullOrBlank()) {
                Toast.makeText(requireContext(), msg, Toast.LENGTH_SHORT).show()
            }
        }

        // API-dən dərsləri yüklə
        viewModel.loadMyBookings()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
